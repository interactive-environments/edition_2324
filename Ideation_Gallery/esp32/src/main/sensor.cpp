#include "sensor.h"

#include "FastLED.h"
#include "log.h"
#include "osc.h"
#include "network.h"
#include "config.h"

namespace sensor {
	Log log("tof", ANSI_ORANGE);
	Log logdebug("tof-debug", ANSI_REDUCED);
	Adafruit_VL53L0X tof = Adafruit_VL53L0X();
	VL53L0X_RangingMeasurementData_t measure;
	double timeout = 0;
	int count = 0;
	bool available = false;

	void setup() {
		if (!tof.begin()) {
			log.error("Failed to boot ToF sensor");
			return;
		}

		available = true;
	}

	void senseDiscovery() {
		int val = range();

		if (millis() - timeout < config::node.cooldown) {
			if (val > config::node.threshold) {
				if (timeout > 0) {
					EVERY_N_MILLIS(10) {
						timeout -= 100;
					}
				}
				logdebug("timeout, waiting %f", config::node.cooldown - (millis() - timeout));
			}
			return;
		}

		if (count >= 2) {
			count = 0;
			if (network::online() && OSC::online) {
				if (val != -1 && val < config::node.threshold) {
					timeout = millis();
					log("sending discovery, tof %d", val);
					OSC::sendDiscovery(0.7 + 0.3 * ((config::node.threshold - val)/config::node.threshold));
				}
			}
		} else {
			++count;
		}
	}

	int range() {
		if (!available) {
			EVERY_N_SECONDS(30) {
				setup();
				return range();
			} else {
				return -1;
			}
		}

		tof.rangingTest(&measure, false);
		if (measure.RangeStatus == 4) {
			return -1; // phase failures have incorrect data
		}
		logdebug("%dmm (status %d)", measure.RangeMilliMeter, measure.RangeStatus);
		return measure.RangeMilliMeter;
	}
};
