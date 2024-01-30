# NeoPixel.py

import time
import board
import neopixel

class NeopixelLED:

    # RGB values
    GREEN = 0
    RED = 0
    BLUE = 0
    WHITE = 0

    # Whether the RGB value should go up or down
    ascending = False

    # Initial study time, used for ripe function
    max_minutes = 0

    def __init__(self, num_leds = 1 ,port_leds=board.D13, brightness=1):
        self.pin_leds = port_leds
        self.num_leds = num_leds
        self.leds = neopixel.NeoPixel(self.pin_leds, self.num_leds, auto_write=True, pixel_order=neopixel.GRBW, brightness=brightness)


    # Update the LED with specified intensity for all three color channels
    def update(self, color):
        intensity = max(color[0], max(color[1], color[2]))
        color = max(0, min(intensity, 255))
        self.leds.fill((color, color, color, color))


    # Update the LED with a tuple of (RED, GREEN, BLUE, WHITE)
    def update_full_color(self, color):
        clipped_color = (max(0, min(color[0], 255)),
            max(0, min(color[1], 255)),
            max(0, min(color[2], 255)),
            max(0, min(color[3], 255)))
        self.leds.fill(clipped_color)


    # Makes the led pulsate blue, the higher the steps, the faster the cycle
    def pulse_blue(self, steps):

        self.RED = 0
        self.GREEN = 0

        if not self.ascending:
            self.BLUE -= steps
            self.ascending = self.BLUE < 0
            self.update_full_color((self.RED, self.GREEN, self.BLUE, self.WHITE))
        else:
            self.BLUE += steps
            self.ascending = self.BLUE < 255
            self.update_full_color((self.RED, self.GREEN, self.BLUE, self.WHITE))


    # Makes the led pulsate red, the higher the steps, the faster the cycle
    def pulse_red(self, steps):

        self.BLUE = 0
        self.GREEN = 0

        if not self.ascending:
            self.RED -= steps
            self.ascending =  self.RED < 0
            self.update_full_color((self.RED, self.GREEN, self.BLUE, self.WHITE))
        else:
            self.RED += steps
            self.ascending = self.RED < 255
            self.update_full_color((self.RED, self.GREEN, self.BLUE, self.WHITE))
    

    # Makes the led act like a riping tomato
    def ripe(self, studying_time):

        self.BLUE = 0

        # Set value to max_minutes variable
        if (studying_time > self.max_minutes):
            self.max_minutes = studying_time
        
        # Use passage of time in ordert to change the led color
        self.RED = int(150 + (105 * (1 - (studying_time / self.max_minutes )))) 
        self.GREEN = int(255 * (studying_time / self.max_minutes))

        self.update_full_color((self.RED, self.GREEN, self.BLUE, self.WHITE))


    def flash_red_blue(self):

        self.GREEN = 0

        for _ in range(2):
            self.RED = 255
            self.BLUE = 0
            for val in range(255):
                self.update_full_color((val, self.GREEN, 255 - val, self.WHITE))

            self.BLUE = 255
            self.RED = 0
            for val in range(255):
                self.update_full_color((255 - val, self.GREEN, val, self.WHITE))

    def flash_green_blue(self):

        self.RED = 0

        for val in range(255):
            self.update_full_color((self.RED, val, self.BLUE, self.WHITE))

        for _ in range(2):
            self.GREEN = 255
            self.BLUE = 0
            for val in range(255):
                self.update_full_color((self.RED, 255 - val, val, self.WHITE))

            self.BLUE = 255
            self.GREEN = 0
            for val in range(255):
                self.update_full_color((150, val, 255 - val, self.WHITE))