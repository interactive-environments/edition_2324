# Tof.py

import time
import board
import busio
import adafruit_vl53l0x

class Tof():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)

    def sense(self, distance):
        return self.vl53.range < distance and self.vl53.range > 20

    def sense_range(self):
        return self.vl53.range
