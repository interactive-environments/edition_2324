#include "pulses.h"
#include "osc.h"
#include "log.h"
#include "sky.h"
#include "config.h"
#include <sys/_stdint.h>

#define DIR_SEND 0
#define DIR_RECV 1

#define MAX_WIDTH 21
#define MIN_WIDTH 2

namespace pulses {
	Log log("pulse");
	Log logLed("pulse:led", ANSI_CYAN, true);
	std::list<Pulse> pulses;
	SemaphoreHandle_t pMutex = NULL;
 	StaticSemaphore_t pMutexBuffer;

	void setup() {
		pMutex = xSemaphoreCreateMutexStatic(&pMutexBuffer);
		OSC::addRoute("/discoveryPoint", pulses::handleDiscoveryPoint);
	}

	void handleDiscoveryPoint(OSCMessage &msg) {
		// type: sfiiii
		// tag, intensity, startTs, endTs, startLed, endLed
		if (!msg.isString(0) || !msg.isFloat(1) || !msg.isInt(2) || !msg.isInt(3) || !msg.isInt(4) || !msg.isInt(5)) {
			log("dropping malformed /discoveryPoint");
			return;
		}

		if (!sky::clock.hasSync()) {
			log("received pulse but not skyclock sync yet, dropping");
			return;
		}

		double time = sky::clock.get();

		char buf[16];
		msg.getString(0, buf, sizeof(buf));
		std::string tag = buf;

		float intensity = msg.getFloat(1);
		double startTs = msg.getInt(2);
		if (startTs < time) {
			log("corrected start time to current time");
			startTs = time;
		} else {
			startTs = startTs / 10000.0;
		}
		double endTs = msg.getInt(3) / 10000.0;
		int startLed = msg.getInt(4);
		int endLed = msg.getInt(5);

		bool forwards = startLed < endLed;

		log(
			"discoveryPoint '%s' (%x), dir %s, intensity %.2f",
			tag.c_str(),
			config::tags[tag],
			forwards ? "send" : "recv",
			intensity
		);
		log(
			"  startTs %.3f endTs %.3f (ttl %.3f) leds (%d:%d)",
			startTs, endTs, endTs - startTs,
			startLed, endLed
		);

		if (time > endTs) {
			log("  dropping discovery, too old");
			return;
		}

		uint8_t width = MIN_WIDTH + round((MAX_WIDTH - MIN_WIDTH) * intensity);
		uint8_t resolution = std::ceil(255 / width);

		double distance = (abs(startLed - endLed) * resolution);
		double speed = distance / (endTs - startTs);
		log("  travels distance %.0f, with speed %.0f", distance, speed);

		endTs += (3 * width * resolution) / speed + 1;
		log("  endTs updated to %f", endTs);

		double startOffset = startLed * resolution;

		if (forwards) {
			startOffset -= width * resolution;
		} else {
			startOffset += width * resolution;
		}

		int minLed = max(0, forwards
			? startLed
			: endLed);
		int maxLed = min(config::node.leds, forwards
			? endLed
			: startLed);

		CRGB _color = config::tags[tag];
		CHSV color = rgb2hsv_approximate(config::tags[tag]);
		// log("  pulse color: (%d,%d,%d) HSV (%d,%d,%d) val %f", _color.r, _color.g, _color.b, color.h, color.s, color.v, 0.3 + intensity);
		color.v = color.v * (min(1.0, 0.3 + intensity));
		// log(" with intensity factor: (%d,%d,%d)", color.h, color.s, color.v);
		// color.fadeToBlackBy((1 - intensity) * 215);

		if (xSemaphoreTake(pMutex, 100)) {
			pulses.push_front(Pulse{
				forwards,
				startTs,
				endTs,
				speed,
				startOffset,
				width,
				resolution,
				minLed,
				maxLed,
				color
			});

			xSemaphoreGive(pMutex);
		} else {
			log.error("could not get pulses mutex, dropping");
		}
	}

	void renderPulses(CHSV ledsHSV[], double time) {
		fill_solid(ledsHSV, config::node.leds, CHSV(0, 0, 0));
		int pIndex = 0;
		for (auto iter = pulses.begin(); iter != pulses.end();) {
			auto p = *iter;
			if (time > p.endTs) {
				if (xSemaphoreTake(pMutex, 0)) {
					logLed("removing %d", pIndex);
					iter = pulses.erase(iter);
					xSemaphoreGive(pMutex);
					continue;
				} else {
					log.error("could not get pulses mutex, not deleting");
				}
			}

			++iter;
			++pIndex;

			double position = p.speed * (time - p.startTs);
			if (p.forwards) {
				position = p.startOffset + position;
			} else {
				position = p.startOffset - position;
			}

			int pos = std::floor(position / p.resolution);
			// logLed("position %f (%d (min: %d max: %d)) (start: %f)", position, pos, p.minLed, p.maxLed, p.startOffset);

			if (pos < p.minLed - p.width-3 || pos > p.maxLed + p.width + 2) {
				// logLed("  skipping");
				continue;
			}

			// .007480ms, .007469ms
			int dist = abs((pos * p.resolution) - position);

			//TODO: break condition is ideal for forward pulse,
			// for backwards it would be slightly more efficient to start for loop
			// at p.width+1 and go down from there, reversing break/continue statements
			int posI = pos - p.width;
			for (int offset = -1 * p.width -1; offset <= p.width + 2; offset++) {
				// int posI = pos + offset;
				if (posI > p.maxLed) {
					// logLed("posI %d > p.maxLed %d", posI, p.maxLed);
					break;
				} else if (posI < p.minLed) {
					// logLed("posI %d < p.minLed %d", posI, p.minLed);
				} else {
					int val = (p.resolution * offset);

					if (offset <= 0) {
						val = dist - val;
					} else {
						val = val - dist;
					}

					// logLed("led %d", posI);

					if (val < 255) {
						CHSV color = CHSV(p.color);
						color.v = color.v * (1.0 - val/255.0);
						if (ledsHSV[posI].v > 0) {
							uint8_t hue = color.h + ledsHSV[posI].h;
							// logLed("  mixing (%d, %d, %d) with (%d, %d, %d)", color.h, color.s, color.v, ledsHSV[posI].h, ledsHSV[posI].s, ledsHSV[posI].v);
							float valRatio = (float)color.v / (float)(color.v + ledsHSV[posI].v);
							uint8_t minHue = min(color.h, ledsHSV[posI].h);
							uint8_t diff = abs(color.h - ledsHSV[posI].h);
							// logLed("  ratio %f %d %d", valRatio, minHue, diff);
							if (diff > 128) {
								color.h = minHue - diff * valRatio;
							} else {
								color.h = minHue + diff * valRatio;
							}
							// logLed("  res: %d", color.h);
							// color.h = valRatio * color.h + (1-valRatio)*ledsHSV[posI].v;
							color.s = (color.s + ledsHSV[posI].s)/2;
							// color.s = min(color.s, ledsHSV[posI].s) + valRatio * color.s;
							color.v = max(color.v, ledsHSV[posI].v);
							// if (ledsHSV[posI].v < color.v) {
							// 	ledsHSV[posI] = color;
							// }
						}

						ledsHSV[posI] = color;
						// logLed("  %d: (%d, %d, %d)", posI, ledsHSV[posI].h, ledsHSV[posI].s, ledsHSV[posI].v);
					}

					// if (val >= 255) {
					// 	ledsHSV[posI] = CHSV(0, 0, 0);
					// } else {
					// 	// ledsHSV[posI] = CRGB(p.color).fadeToBlackBy(val);
					// }
				}

				++posI;
			}
		}
	}
}