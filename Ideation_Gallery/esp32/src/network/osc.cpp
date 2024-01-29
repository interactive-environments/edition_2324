#include "osc.h"

#include "WiFi.h"
#include "WiFiUdp.h"
#include <vector>
#include <functional>

#include "OSCMessage.h"
#include "FastLED.h"

#include "log.h"
#include "config.h"
#include "network.h"

struct OSCRoute {
	char const * route;
	RouteFunction func;
};

namespace OSC {
	Log log("osc", ANSI_GREEN);
	WiFiUDP udp;
	bool online = false;
	std::vector<OSCRoute> routes;

	void listen() {
		int err;
		if ((err = udp.begin(1212)) > 0) {
			log("Listening on %s:1212", WiFi.localIP().toString().c_str());
			online = true;
			// Serial.printf("[osc] Listening on %s:1212\r\n", WiFi.localIP().toString().c_str());
		} else {
			log.error("Failed to open port 1212: %d", err);
		}

		// udpClient.begin(1214);
	}

	void addRoute(const char *route, RouteFunction func) {
		log("added handler for route %s", route);
		routes.push_back(OSCRoute{route, func});
	}

	void sendDiscovery(float intensity) {
		OSCMessage msg("/discoveryPoint");

		msg.add(config::node.x);
		msg.add(config::node.y);
		msg.add(config::node.z);
		msg.add(intensity);
		msg.add(config::hostname.c_str());

		udp.beginPacket(network::centralHostIp.c_str(), 1212);
		msg.send(udp);
		udp.endPacket();
	}

	void loop() {
		int packetSize = udp.parsePacket();
		if (packetSize) {
			log("Received packet from %s (len=%d)", udp.remoteIP().toString().c_str(), packetSize);

			OSCMessage msg;
			while (packetSize--) {
				msg.fill(udp.read());
			}

			if (msg.hasError()) {
				log.error("Error decoding (%d)", msg.getError());
			} else {
				bool matched = false;
				for (OSCRoute r : routes) {
					if (msg.dispatch(r.route, r.func)) {
						matched = true;
						break;
					}
				}
				if (!matched) {
					char addr[64];
					msg.getAddress(addr);
					log("'%s' matched no routes", addr);
				}
				// msg.dispatch("/test", testMessage);
			}
		// } else if (config::node.type == "spiral") {
		// 	EVERY_N_SECONDS(2) {
		// 		if (random(0, 5) < 1) {
		// 			log("sending /discoveryPoint");
		// 			sendDiscovery(random(0, 30)/100.0);
		// 		}
		// 	}
		}
	}
}
