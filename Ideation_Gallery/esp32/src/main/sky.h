#ifndef _sky_h_
#define _sky_h_

#include "esp32-hal.h"

class SkyClock {
	double _lastUpdate;
	double clock = 0;
	bool synced = false;

	public:
		void update(int time) {
			synced = true;
			_lastUpdate = millis();
			clock = time / 10000.0;
		}

		float get() {
			return clock + (millis() - _lastUpdate)/10000.0;
		}

		bool hasSync() {
			return synced;
		}
};

namespace sky {
	extern SkyClock clock;
	void setup();
}

#endif
