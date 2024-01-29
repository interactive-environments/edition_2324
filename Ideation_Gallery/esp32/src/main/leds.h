#ifndef _leds_h
#define _leds_h

#include "FastLED.h"
#include <sys/_stdint.h>

#define NUM_LEDS 121
#define BRIGHTNESS 255

namespace ledstrip {
	extern CRGB leds[NUM_LEDS];
	extern CHSV ledsHSV[NUM_LEDS]; 
	extern CRGB statusLed[1];

	void status(uint8_t r, uint8_t g, uint8_t b);
	void setup();
}

class Leds {
	public:
	uint _offset;
	uint _num_leds;

	Leds(uint offset, uint num_leds) {
		_offset = offset;
		_num_leds = num_leds;
	};

	void update() {
		// fill_rainbow(leds+_offset, _num_leds, 0, 5);
		// FastLED.show();
	};
};

#endif
