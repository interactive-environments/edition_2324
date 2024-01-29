#ifndef _sensor_h
#define _sensor_h

#include "Adafruit_VL53L0X.h"

namespace sensor {
	extern double timeout;
	void setup();
	int range();
	void senseDiscovery();
}

#endif