#include "config.h"

#include "esp_mac.h"
#include "log.h"
#include <string>
#include "SPIFFS.h"

#include <fstream>
#include <sstream>
#include <string>

#include "log.h"
#include "leds.h"

#define FORMAT_SPIFFS_IF_FAILED true
/* IMPORTANT: SPIFFS paths NEED to start with /spiffs/ to use ifstream/ofstream */

using namespace nlohmann;

namespace config {
	Log log("config", ANSI_GRAY);
	std::string hostname;
	NodeConfig node;
	TagList tags;

	void configureHostname() {
		std::ifstream input("/spiffs/host");
		if (input.is_open()) {
			std::stringstream buf;
			buf << input.rdbuf();
			config::hostname = buf.str();
		} else {
			input.close();
			log("/host does not exist, generating from mac");

			unsigned char mac_base[6] = {0};
			esp_efuse_mac_get_default(mac_base);
			char buf[5 + 6]; // 'node-', octet, -, octet
			snprintf(buf, sizeof(buf), "node-%02X-%02X", mac_base[4], mac_base[5]);
			hostname = buf;

			std::ofstream output("/spiffs/host");
			output << config::hostname;
			output.close();
		}
	}

	template <typename T> T readJSON(const char* filename) {
		T asClass;
		log("reading %s", filename);

		std::ifstream input(filename);

		if (input.is_open()) {
			try {
				json data;
				input >> data;
				asClass = data;
			} catch (const json::exception& e) {
				log.error("failed to parse json %s: %s", filename, e.what());
			}
		} else {
			log.error("failed to read '%s'", filename);
		}
		return asClass;
	}

	template <typename T> T parseJSON(const char* filename, T currentCfg, const char* data) {
		log("parsing json before write to %s", filename);
		json newCfg = json::parse(data);

		if (newCfg == (json)currentCfg) {
			log("config %s identical", filename);
			return currentCfg;
		} else {
			log("updating %s", filename);
			std::ofstream output(filename);

			if (output.is_open()) {
				output << data;
				log("wrote %d bytes to %s", (int)output.tellp(), filename);
			} else {
				log.error("failed to write to %s", filename);
			}

			return (T)newCfg;
		}
	}

	void receiveConfig(char * data) {
		node = parseJSON<NodeConfig>("/spiffs/config.json", node, data);
	}

	void receiveTags(char * data) {
		tags = parseJSON<TagList>("/spiffs/tags.json", tags, data);
	}

	void load() {
		if (!SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED)) {
			log("failed to mount SPIFFS");
			return; // TODO: handle more gracefully?
		}

		configureHostname();

		node = readJSON<NodeConfig>("/spiffs/config.json");
		tags = readJSON<TagList>("/spiffs/tags.json");

		log("config: x %d, y %d, z %d", node.x, node.y, node.z);
		for (auto tag : node.tags) {
			log("  tag: %s (%x)", tag.c_str(), tags[tag]);
		}
	}
}