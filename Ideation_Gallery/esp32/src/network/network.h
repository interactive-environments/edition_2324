#ifndef _network_h
#define _network_h

#include <string>

namespace network {
	extern std::string centralHostIp;
	void setup();
	void discoverServer();
	bool online();
}

#endif
