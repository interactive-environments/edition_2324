#ifndef _config_h
#define _config_h

#include "nlohmann/json.hpp"
#include <string>

class NodeConfig {
	public:
		int x = 0;
		int y = 0;
		int z = 0;
		int leds = 0;
		std::vector<std::string> tags = {};
		std::string type = "spiral";
		bool staging = false;
		bool sensor = false;
		int cooldown = 10000;
		int threshold = 8000;
		NodeConfig() = default;
		NLOHMANN_DEFINE_TYPE_INTRUSIVE_WITH_DEFAULT(NodeConfig, x, y, z, leds, tags, type, staging, sensor, cooldown, threshold)
};

typedef std::map<std::string, int> TagList;

namespace config {
	extern std::string hostname;
	extern NodeConfig node;
	extern TagList tags;

	void load();
	void receiveConfig(char* data);
	void receiveTags(char* data);
}

#endif
