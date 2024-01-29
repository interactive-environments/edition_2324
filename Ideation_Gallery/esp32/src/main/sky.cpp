#include "sky.h"

#include "OSCMessage.h"
#include "log.h"
#include "osc.h"

namespace sky {
	Log log("sky", ANSI_BLUE);
	SkyClock clock;

	void receiveSkyParams(OSCMessage &msg) {
		log("receiving skyParams");
	}

	void receiveSkyClock2(OSCMessage &msg) {
		if (!msg.isInt(0)) {
			return log.error("skyClock2 update did not contain integer");
		}

		clock.update(msg.getInt(0));

		log("updated skyClock2 to %f", clock.get());
	}

	void setup() {
		OSC::addRoute("/skyClock2", receiveSkyClock2);
		OSC::addRoute("/skyParams", receiveSkyParams);
	};
}
