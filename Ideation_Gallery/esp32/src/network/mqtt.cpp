#include "mqtt.h"

#include <array>
#include <functional>
#include <string>

#include "nlohmann/json.hpp"
#include "PubSubClient.h"

#include "config.h"
#include "log.h"
#include "version.h"

using namespace nlohmann;

namespace MQTT {
	Log log("mqtt", ANSI_PURPLE);
	WiFiClient wifiClient;
	PubSubClient mqtt(wifiClient);
	std::string nodeOnlineTopic = "/nodes/"; // + <name> + "/online"

	CallbackFunction mqttCallbackServerOnline;
	CallbackFunction mqttCallbackConfig;
	CallbackFunction mqttCallbackTagsConfig;

	std::map<std::string, CallbackFunctionPtr> callbacks{
		{"/nodes/server/online", mqttCallbackServerOnline},
		{"/config/tags", mqttCallbackTagsConfig}
	};

	void mqttCallback(char* topic, byte* message, unsigned int length) {
		char* msg = new char[length+1];
		for (int i = 0; i < length; i++) {
			msg[i] = message[i];
		}
		msg[length] = '\0';

		log("received %s %s", topic, msg);

		bool matched = false;
		for (const auto& [route, callback] : callbacks) {
			const char* strRoute = route.c_str();
			int routeLen = strlen(strRoute);
			if (strncmp(topic, strRoute, routeLen) == 0) {
				log("handled by %s", strRoute);
				if (callback(topic + routeLen, msg)) {
					matched = true;
					break;
				}
			}
		}
		if (!matched) {
			log("%s matched no routes", topic);
		}
	}

	void setup() {
		nodeOnlineTopic += config::hostname;
		nodeOnlineTopic += "/online";

		std::string configTopic = "/nodes/";
		configTopic += config::hostname;
		configTopic += "/config";
		callbacks[configTopic] = &mqttCallbackConfig;

		wifiClient.setTimeout(5000);
		mqtt.setCallback(mqttCallback);
	}

	void onlineStatus() {
		log("sending online status");
		json obj;
		obj["version"] = version::version;

		obj["osc"]["host"] = wifiClient.localIP().toString().c_str();
		obj["osc"]["port"] = 1212;

		std::string serialized = obj.dump();
		mqtt.publish(nodeOnlineTopic.c_str(), serialized.c_str());
	}

	bool connect() {
		log("connecting...");
		// connects with cleanSession true
		bool success = mqtt.connect(
			config::hostname.c_str(),
			NULL, NULL,
			NULL, 0, 0, NULL, true
		);
		// cleanSession false (default)
		// bool success = mqtt.connect(config::hostname.c_str());

		if (success) {
			log("connected");
			onlineStatus();
			for (const auto& [route, callback] : callbacks) {
				std::string topic = route;
				if (topic.back() == '/') {
					topic += "#";
				}
				log("  - subscribed to '%s'", topic.c_str());
				mqtt.subscribe(topic.c_str());
			}
		} else {
			log.error("connection failure (%d)", mqtt.state());
		}

		return success;
	}

	void disconnect() {
		mqtt.disconnect();
	}

	void setServer(const char* server, int port) {
		mqtt.setServer(server, port);
	}

	int loop() {
		return mqtt.loop();
	}

	bool isConnected() {
		return mqtt.connected();
	}

	void addRoute(std::string route, CallbackFunctionPtr callback) {
		callbacks[route] = callback;

		if (isConnected()) {
			std::string topic = route;
			if (topic.back() == '/') {
				topic += "#";
			}
			log("subscribed to '%s'", topic.c_str());
			mqtt.subscribe(topic.c_str());
		}
	}

	bool mqttCallbackServerOnline(char* target, char* msg) {
		log("server online, re-broadcasting status");
		onlineStatus();
		CentralLogger::reconnect();

		return true;
	}

	bool mqttCallbackConfig(char* _topic, char* data) {
		config::receiveConfig(data);
		return true;
	}

	bool mqttCallbackTagsConfig(char* _topic, char* data) {
		config::receiveTags(data);
		return true;
	}
}

