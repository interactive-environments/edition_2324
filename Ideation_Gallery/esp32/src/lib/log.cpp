#include "log.h"
#include <cstdarg>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <sys/_stdint.h>
#include "WiFiClient.h"
#include <vector>

#include "config.h"
#include "sky.h"

namespace CentralLogger {
	Log log("log", ANSI_ORANGE);
	WiFiClient _wifiClient;

	bool _networked = false;
	double _connectAttempt = 0;
	const char* _server;
	int _port;

	void connectServer(const char* server, int port) {
		_connectAttempt = millis();
		_server = server;
		_port = port;
		_wifiClient.stop();
		int res = _wifiClient.connect(server, port, 5000);
		if (res) {
			_wifiClient.printf("++connect: %s\r\n", config::hostname.c_str());
			log("Connected to central logging server (%s:%d)", server, port);
		} else {
			log.error("Error connecting to central logging server %s:%d (%d)", server, port, res);
		}

		_networked = true;
	};

	void reconnect() {
		if (millis() - _connectAttempt > 30000) { // every 30 sec
			connectServer(_server, _port);
		}
	}

	void disconnectServer() {
		_wifiClient.stop();
	}

	bool isNetworked() {
		return _networked;
	}
}

Log::Log(const char* name, const char* color, bool localOnly) {
	snprintf(_name, sizeof(_name), "%s[%s]%s", color, name, ANSI_DEFAULT);
	snprintf(_errorName, sizeof(_errorName), "%s[%s:%sERROR%s]%s", color, name, ANSI_RED, color, ANSI_DEFAULT);
	_localOnly = localOnly;
}

static const char* const final_format = "%s%s%7.3f%s %s %s\r\n"; // ~0.00 [name] str\r\n

void Log::write(const char* fmt, va_list arg, bool isError) {
	va_list copy;
	va_copy(copy, arg);
	// initialize vector with size (1 + length)
	std::vector<char> buf(1 + vsnprintf(nullptr, 0, fmt, arg));
	vsnprintf(buf.data(), buf.size(), fmt, copy);
	va_end(copy);

	std::vector<char> buf2(1 + snprintf(nullptr, 0, final_format,
		ANSI_REDUCED,
		sky::clock.hasSync() ? "" : "~",
		sky::clock.get(),
		ANSI_DEFAULT,
		isError
			? _errorName
			: _name,
		buf.data()
	));

	snprintf(buf2.data(), buf2.size(), final_format,
		ANSI_REDUCED,
		sky::clock.hasSync() ? "" : "~",
		sky::clock.get(),
		ANSI_DEFAULT,
		isError
			? _errorName
			: _name,
		buf.data()
	);

	if (Serial.availableForWrite()) {
		Serial.write(buf2.data(), buf2.size());
	}

	if (!_localOnly && CentralLogger::isNetworked()) {
		if (!CentralLogger::_wifiClient.connected()) {
			CentralLogger::reconnect();
		}
		CentralLogger::_wifiClient.write(buf2.data(), buf2.size());
	}
}

void Log::operator()(const char* fmt, ...) {
	va_list arg;
	va_start(arg, fmt);
	Log::write(fmt, arg);
	va_end(arg);
}

void Log::error(const char* fmt, ...) {
	va_list arg;
	va_start(arg, fmt);
	Log::write(fmt, arg, true);
	va_end(arg);
}
