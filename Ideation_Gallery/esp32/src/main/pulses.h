#ifndef _pulses_h
#define _pulses_h

#include <sys/_stdint.h>
#include <list>
#include "FastLED.h"
#include "osc.h"

struct Pulse {
	bool forwards;
	double startTs;
	double endTs;
	double speed;
	double startOffset;
	uint8_t width;
	uint8_t resolution;
	int minLed;
	int maxLed;
	CHSV color;
};

namespace pulses {
	void setup();
	void handleDiscoveryPoint(OSCMessage &msg);
	void renderPulses(CHSV ledsHSV[], double time);
}

#endif