# NeoPixel.py

import time
import board
import neopixel

class NeopixelLED():
    def __init__(self, num_leds = 1,port_leds=board.D13):
        self.pin_leds = port_leds
        self.num_leds = num_leds
        self.leds = neopixel.NeoPixel(self.pin_leds, self.num_leds, auto_write=False, pixel_order=neopixel.GRBW)
        print("setup")

    # Update the LED with specified intensity for all three color channels
    def update(self, color):
        intensity = max(color[0], max(color[1], color[2]))
        color = max(0, min(intensity, 255))
        self.leds.fill((color, color, color, color))
        self.leds.show()

    # Update the LED with a tuple of (RED, GREEN, BLUE, WHITE)
    def update_full_color(self, color):
        clipped_color = (max(0, min(color[0], 255)),
            max(0, min(color[1], 255)),
            max(0, min(color[2], 255)),
            max(0, min(color[3], 255)))
        self.leds.fill(clipped_color)
        self.leds.show()
