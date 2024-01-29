#include "Arduino.h"

#include "config.h"
#include "reset_reason.h"
#include "./main/main.h"
#include "./network/network.h"
#include "log.h"
#include "./main/leds.h"
#include "rom/rtc.h"
#include "version.h"

void setup() {
	heap_caps_malloc_extmem_enable(4096);
	Serial.begin(115200);
	Log log("system", ANSI_GRAY);
	log("boot %s (%s)", version::version, version::env);
	log("CPU0 reset:");
	verbose_print_reset_reason(rtc_get_reset_reason(0));
	log("CPU1 reset:");
	verbose_print_reset_reason(rtc_get_reset_reason(1));
	log("heap: %i", ESP.getFreeHeap());
	log("psram: %i", ESP.getFreePsram());
	log("sketch: %i", ESP.getFreeSketchSpace());

	ledstrip::setup();
	ledstrip::status(255, 97, 184);
	config::load();
	ledstrip::status(255, 128, 0);
	network::setup();
	main::setup();
}

void loop() {
	main::loop();
}
