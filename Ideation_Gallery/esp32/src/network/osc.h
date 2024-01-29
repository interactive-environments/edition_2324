#ifndef _osc_h
#define _osc_h

#include "OSCMessage.h"
#include <functional>

// typedef std::function<void (OSCMessage &msg)> RouteFunction;
typedef void (*RouteFunction)(OSCMessage &);

namespace OSC {
	extern bool online;
	void listen();
	void loop();
	void addRoute(const char* route, RouteFunction func);
	void sendDiscovery(float intensity);
}

#endif
