#include "network.h"

// ESP-IDF v5.1 gives looots of warnings without this
// #pragma GCC diagnostic push 
// #pragma GCC diagnostic ignored "-Wattributes"
#include "FreeRTOS.h"
#include "WiFiClient.h"
#include "esp_err.h"
#include "freertos/task.h"
// #pragma GCC diagnostic pop
#include "esp_task_wdt.h"

#include "WiFi.h"
#include "WiFiMulti.h"
#include "mdns.h"

#include "config.h"
#include "secrets.h"
#include "http-ota.h"
#include "mqtt.h"
#include "osc.h"
#include "log.h"
#include "leds.h"

#include "FastLED.h"

#define LOG_HOST "192.168.1.102" // ouroboros

namespace network {
	WiFiClient wifiClient;
	WiFiMulti wifiMulti;
	xSemaphoreHandle sLog = NULL;
	Log log("network", ANSI_CYAN);

	const char* centralHost = "ideation-pi";
	std::string centralHostIp = "192.168.1.101"; /* fallback default ip */

	bool isReconnect = true;
	bool firstConnect = true;

	void networkTask(void * pvParameters) {
		esp_task_wdt_init(20, true);
		esp_err_t err = esp_task_wdt_add(NULL);

		WiFi.persistent(true);

		log("configured WiFi networks:");
		for (auto w: wifiNetworks) {
			if (strlen(w[0]) > 0) {
				log("  - %s", w[0]);
				wifiMulti.addAP(w[0], w[1]);
			}
		}

		httpOTA::setup();
		MQTT::setup();

		while (true) {
			if (wifiMulti.run() != WL_CONNECTED) {
				isReconnect = true;
				log.error("lost WiFi... reconnecting");
				ledstrip::status(255, 0, 0);
				delay(1000);
				continue;
			} else if (isReconnect) {
				isReconnect = false;
				log("connected to %s as %s", WiFi.SSID().c_str(), WiFi.localIP().toString().c_str());
				ledstrip::status(0, 5, 0);

				#ifdef LOG_HOST
				CentralLogger::connectServer(LOG_HOST, 1337);
				#else
				CentralLogger::connectServer(centralHostIp.c_str(), 1337);
				#endif

				MQTT::setServer(centralHostIp.c_str(), 1883);

				OSC::listen();
				MQTT::connect();

				esp_task_wdt_reset();
			}

			while (!MQTT::isConnected()) {
				if (!MQTT::connect()) {
					discoverServer();
				}
			}

			if (firstConnect && online()) {
				// set status led, increase network watchdog to 120 seconds
				log("online!");
				esp_task_wdt_init(120, true);
				firstConnect = false;
			}

			OSC::loop();
			MQTT::loop();

			EVERY_N_SECONDS(60) {
				log("temperature: %.2f", temperatureRead());
			}

			esp_task_wdt_reset();
			vTaskDelay(1);
		}
	}

	void setup() {
		log("%s", config::hostname.c_str());
 		xTaskCreatePinnedToCore(networkTask, "network", 4096, NULL, 3, NULL, 0);
	}

	bool online() {
		return (wifiMulti.run() == WL_CONNECTED && !isReconnect);
	}

	void discoverServer() {
		esp_err_t err = mdns_init();
		if (err){
			log.error("mDNS failure (%s)", esp_err_to_name(err));
			return;
		}

		struct esp_ip4_addr addr;
		addr.addr = 0;

		log("mDNS query for '%s'", centralHost);
		err = mdns_query_a(centralHost, 2000, &addr);

		if (err == ESP_ERR_NOT_FOUND){
			log.error("server was not found!");
			return;
		} else if (err) {
			log.error("mDNS query failed (%s)", esp_err_to_name(err));
			return;
		}

		centralHostIp = IPAddress(addr.addr).toString().c_str();
		log("mDNS discovery for '%s' at %s", centralHost, centralHostIp.c_str());

		#ifdef LOG_HOST
		CentralLogger::connectServer(LOG_HOST, 1337);
		#else
		CentralLogger::connectServer(centralHostIp.c_str(), 1337);
		#endif

		MQTT::setServer(centralHostIp.c_str(), 1883);
	}
}
