#ifndef _log_h
#define _log_h

#include "WiFiClient.h"
#include <string>

#define ANSI_DEFAULT "\033[0m"
#define ANSI_RED "\033[31;1m"
#define ANSI_GREEN "\033[32;1m"
#define ANSI_ORANGE "\033[33;1m"
#define ANSI_BLUE "\033[34;1m"
#define ANSI_PURPLE "\033[35;1m"
#define ANSI_CYAN "\033[36;1m"
#define ANSI_GRAY "\033[37;1m"
#define ANSI_REDUCED "\033[39;2m"

namespace CentralLogger {
	bool isNetworked();
	void connectServer(const char* host, int port);
	void reconnect();
	void disconnectServer();
}

class Log {
	// const char* _name;
	char _name[64];
	char _errorName[64];
	bool _localOnly;
	void write(const char *format, va_list args, bool isError = false);

	public:
		Log(const char *name, const char *color = "", bool localOnly = false);

		void operator()(const char *format, ...) __attribute__ ((format (printf, 2, 3)));
		void error(const char *format, ...) __attribute__ ((format (printf, 2, 3)));
};

#endif
