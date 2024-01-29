#include "http-ota.h"

#include "esp_task_wdt.h"
#include "HTTPUpdate.h"

#include "config.h"
#include "log.h"
#include "leds.h"
#include "mqtt.h"

using namespace ledstrip;

namespace httpOTA {
	Log log("ota", ANSI_ORANGE);
	Log logLocal("ota", ANSI_ORANGE, true);
	WiFiClient wifiClient;
	bool inProgress = false;

	void onStarted();
	void onProgress(int, int);
	void onFinished();
	void onError(int);

	bool mqttCallbackOTA(char* target, char* url) {
		if (
			target[0] == '*' ||
			strncmp(config::hostname.c_str(), target, strlen(target)) == 0 ||
			(config::node.staging && (strcmp(target, "dev") == 0))
		) {
			log("heap: %i", ESP.getFreeHeap());
			log("psram: %i", ESP.getFreePsram());
			log("sketch: %i", ESP.getFreeSketchSpace());

			esp_task_wdt_init(120, false);
			inProgress = true;

			t_httpUpdate_return ret = httpUpdate.update(wifiClient, url);

			switch (ret) {
				case HTTP_UPDATE_FAILED:
					log.error("update failed: (%d): %s", httpUpdate.getLastError(), httpUpdate.getLastErrorString().c_str());
					break;

				case HTTP_UPDATE_NO_UPDATES:
					log.error("no updates available");
					break;

				case HTTP_UPDATE_OK:
					log("update success, rebooting...");
					// int a = millis();
					// MQTT::disconnect(); // helps with reconnect after reboot
					// while (MQTT::isConnected()) {
					// 	log("waiting for mqtt to disconnect %lu", millis() - a);
					// }
					delay(500);
					ESP.restart();
					break;
			}

			return true;
		}

		return false;
	}

	void setup() {
		MQTT::addRoute("/ota/", &mqttCallbackOTA);

		httpUpdate.onStart(onStarted);
		httpUpdate.onProgress(onProgress);
		httpUpdate.onEnd(onFinished);
		httpUpdate.onError(onError);
	}

	void onStarted() {
		esp_task_wdt_reset();
		log("starting");
		MQTT::disconnect();
		statusLed[0] = CRGB::Purple;
	}

	void onProgress(int cur, int total) {
		esp_task_wdt_reset();
		int steps = total / 5;

		EVERY_N_SECONDS(1) {
			log("%3d%% (%d / %d)", cur*100/total, cur, total);
		} else {
			logLocal("%3d%% (%d / %d)", cur*100/total, cur, total);
		}

		EVERY_N_MILLIS(100) {
			if (statusLed[0].r == 0) {
				statusLed[0] = CRGB::Yellow;
			} else {
				statusLed[0] = CRGB::Black;
			}
			FastLED.show();
		}
	}

	void onError(int err) {
		log.error("fatal error: %s (%d)", httpUpdate.getLastErrorString().c_str(), err);
		statusLed[0] = CRGB::Red;
		MQTT::connect();
	}

	void onFinished() {
		log("finished");
		statusLed[0] = CRGB::Green;
	}
}
