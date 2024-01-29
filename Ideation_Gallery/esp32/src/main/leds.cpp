#include "leds.h"

#include "config.h"

namespace ledstrip {
	CRGB leds[NUM_LEDS] = {};
	CRGB statusLed[1] = {};
	CHSV ledsHSV[NUM_LEDS] = {};

	void setup() {
		FastLED.addLeds<WS2812, 10, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
		FastLED.addLeds<WS2812, 47, RGB>(statusLed, 1).setCorrection(TypicalLEDStrip);
		FastLED.setBrightness(BRIGHTNESS);
		fill_solid(leds, NUM_LEDS, CRGB::Black);
		fill_solid(ledsHSV, NUM_LEDS, CHSV(0, 0, 0));
		statusLed[0] = CRGB::Black;
		FastLED.show();
	}

	void status(uint8_t r, uint8_t g, uint8_t b) {
		statusLed[0] = CRGB(r, g, b);
		// FastLED.show();
	}
}
