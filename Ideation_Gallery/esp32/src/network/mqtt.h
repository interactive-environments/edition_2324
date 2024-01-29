#ifndef _mqtt_h
#define _mqtt_h

#include "PubSubClient.h"
#include "WiFiClient.h"

#include "http-ota.h"

// typedef bool (CallbackFunction)(char* topic, char* message);
// typedef std::function<bool (char* topic, char* message)> CallbackFunction;
typedef bool (CallbackFunction)(char* topic, char* message);
typedef bool (*CallbackFunctionPtr)(char* topic, char* message);

namespace MQTT {
	void setup();
	bool connect();
	bool isConnected();
	void setServer(const char* server, int port);
	void addRoute(std::string route, CallbackFunctionPtr callback);
	void disconnect();
	int loop();
}

#endif
