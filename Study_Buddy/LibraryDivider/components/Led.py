import neopixel
import time
import random
import board
import math

class Led:

    num_pixels = 3
    brightness = 0.1
    pixels = None

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    BLUE_GREEN = (0, 255, 165)
    ORANGE = (255, 165, 0)


    def __init__(self, pin=board.D10, num_pixels=3, brightness=1.0):

        self.num_pixels = num_pixels
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(
            pin,
            num_pixels,
            brightness=brightness,
            auto_write=True,
            pixel_order=neopixel.GRBW
        )


    def turn_off(self):
        self.pixels.fill((0, 0, 0, 0))

    def color(self, color):
        self.pixels.fill(color)