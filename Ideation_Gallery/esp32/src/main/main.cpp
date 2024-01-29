// Main has all code that runs on the main core / Arduino's loop()
#include "main.h"

#include "FastLED.h"
#include <algorithm>
#include <list>
#include <sys/types.h>
#include <vector>
#include "esp32-hal-gpio.h"
#include "esp32-hal-ledc.h"

#include "http-ota.h"
#include "log.h"
#include "sky.h"
#include "leds.h"
#include "mqtt.h"
#include "sensor.h"
#include "config.h"
#include "pulses.h"

using namespace ledstrip;

namespace main {
	Log log("main", ANSI_BLUE);
	Leds spiral(0, 60);
	uint8_t spot = 255;
	bool blinking = false;
	bool fading = true;

	bool blinkFlag(char* target, char* msg) {
		if (strncmp(config::hostname.c_str(), target, strlen(target)) == 0) {
			if (strcmp(msg, "0") == 0) {
				blinking = false;
			} else if (strcmp(msg, "1") == 0) {
				blinking = true;
			} else if (strcmp(msg, "-1") == 0) {
				blinking = !blinking;
			}

			if (!blinking) {
				ledcWrite(0, 0);
			}

			log("blink request matched, now %s", blinking ? "blinking" : "not blinking");
			return true;
		}
		return false;
	}

	bool setLed(char* target, char* msg) {
		if (strncmp(config::hostname.c_str(), target, strlen(target)) == 0) {
			int led = atoi(msg);
			if (led == -1) {
				fading = true;
				return true;
			}

			if (led < NUM_LEDS) {
				log("setting led %d, currently (%d, %d, %d)", led, leds[led].r, leds[led].g, leds[led].b);
				fading = false;
				// ledsHSV[led] = ledsHSV[led].h == 96 ? CHSV(0, 0, 0) : CHSV(96, 255, 255);
				// showHSV();
			} else {
				log("led %d out of NUM_LED range (%d)", led, NUM_LEDS);
			}
		}

		return true;
	}

	void setup() {
		sky::setup();

		ledcSetup(0, 5000, 12);
		ledcAttachPin(15, 0);

		ledcWrite(0, spot);

		MQTT::addRoute("/debug/blinkFlag/", &blinkFlag);
		MQTT::addRoute("/debug/setLed/", &setLed);
		pulses::setup();

		if (config::node.type == "sensor" || config::node.sensor) {
			sensor::setup();
		}
	}

	void loop() {
		if (httpOTA::inProgress) {
			return;
		}

		if (config::node.type == "sensor" || config::node.sensor) {
			sensor::senseDiscovery();
		}

		if (config::node.leds == 0) {
			return;
		}

		// EVERY_N_SECONDS(1) {
		// 	fill_solid(ledsHSV, config::node.leds, CHSV(0, 0, 0));
		// }

		double time = sky::clock.get();

		pulses::renderPulses(ledsHSV, time);

		if (blinking) {
			if (int(time * 10) % 2 == 0) {
				spot = 0;
			} else {
				spot = 255;
			}

			ledcWrite(0, blinking ? spot : 0);
		}

		hsv2rgb_rainbow(ledsHSV, leds, NUM_LEDS);
		FastLED.show();
	}
}
