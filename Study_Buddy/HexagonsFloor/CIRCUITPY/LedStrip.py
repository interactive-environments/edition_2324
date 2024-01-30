import neopixel
import time
import random
import board
import math

class Led_strip:

    num_pixels = 80
    brightness = 0.1
    pixels = None

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    BLUE_GREEN = (0, 255, 165)
    ORANGE = (255, 165, 0)


    def __init__(self, led_groups, group_colors, pin=board.D10, num_pixels=80, brightness=1):

        self.color_array = []
        self.group_colors = group_colors
        self.led_groups = led_groups
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(
            pin,
            num_pixels,
            brightness=brightness,
            auto_write=True,
            pixel_order=neopixel.GRB
        )

        for i in range(self.num_pixels):
            ratio = i / self.num_pixels
            if ratio <= 0.5:
                color = (
                    int((1 - ratio * 2) * self.BLUE[0] + ratio * 2 * self.BLUE_GREEN[0]),
                    int((1 - ratio * 2) * self.BLUE[1] + ratio * 2 * self.BLUE_GREEN[1]),
                    int((1 - ratio * 2) * self.BLUE[2] + ratio * 2 * self.BLUE_GREEN[2]),
                )
            else:
                ratio = (ratio - 0.5) * 2
                color = (
                    int((1 - ratio) * self.BLUE_GREEN[0] + ratio * self.GREEN[0]),
                    int((1 - ratio) * self.BLUE_GREEN[1] + ratio * self.GREEN[1]),
                    int((1 - ratio) * self.BLUE_GREEN[2] + ratio * self.GREEN[2]),
                )

            self.color_array.append(color)

    def turn_off(self):
        self.pixels.fill((0, 0, 0, 0))

    def sparkle(self, frequency, steps):

        leds_list_length = random.randint(1, 5)  # Leds to turn on at once
        random_indices = []

        while len(random_indices) < leds_list_length:
            num = random.randint(0, self.num_pixels - 1)
            if num not in random_indices:
                random_indices.append(num)

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for i in random_indices:
            self.pixels[i] = color

        # Slowly turn on
        for brightness in range(1, steps + 1):
            self.pixels.brightness = brightness / steps
            time.sleep(0.5)  # Non-blocking sleep

        # Non-blocking random delay before turning off
        time.sleep(random.uniform(0, frequency))

        # Slowly turn off
        for brightness in range(steps, 0, -1):
            self.pixels.brightness = brightness / steps
            time.sleep(0.01)  # Non-blocking sleep

        self.turn_off()

    def fillup(self, steps):

        self.turn_off()

        for i in range(self.num_pixels):
            self.pixels[i] = self.color_array[i]
            time.sleep(steps)

    def flash(self):
        for _ in range(3):
            for i in range(self.num_pixels):
                self.pixels[i] = self.ORANGE
            time.sleep(.5)

            self.turn_off()
            time.sleep(.3)

    def pulse(self, cycles, steps):

        brightness = 1.0

        for _ in range(cycles):

            while brightness > 0.0:
                self.pixels.brightness = brightness
                brightness -= .05
                time.sleep(steps)

            while brightness < 1.0:
                self.pixels.brightness = brightness
                brightness += .05
                time.sleep(steps)

        self.pixels.brightness = self.brightness

    def visual_timer(self, study_time):

        timer_for_each_pixel = study_time / self.num_pixels

        for i in range(self.num_pixels, 0, -1):
            self.pixels[i - 1] = (0, 0, 0 ,0)
            time.sleep(timer_for_each_pixel)

    def wave(self, steps, frequency):

        self.turn_off()
        for step in range(steps):
            for i in range(self.num_pixels):
                # Use a sine function to create a wave pattern for brightness
                brightness = int(127 * math.sin(2 * math.pi * frequency * (i / self.num_pixels - step / steps)) + 128)

                # Update the pixel with calculated brightness
                self.pixels[i] = (brightness, brightness, brightness)
                #self.pixels[i] = self.color_array[i]
                #self.pixels.brightness = brightness

            self.pixels.show()  # Assuming you have a method to update the LEDs
            time.sleep(0.1)  # Adjust the delay between steps as needed

    def woobly(self, window):
        num_pixels = len(self.pixels)
        off = (0, 0, 0)  # Replace with your desired 'off' color
        on = (255, 255, 255)  # Replace with your desired 'on' color

        i = 0
        j = i + window

        while j < num_pixels:
            self.pixels[i] = off
            self.pixels[j] = self.color_array[j]

            i+=1
            j+=1

            time.sleep(0.1)

        j -= 1

        time.sleep(30)

        while i > 0:
            self.pixels[i] = self.color_array[i]
            self.pixels[j] = off

            i -=1
            j -=1

            time.sleep(0.2)

    def jiggly(self, window):
        num_pixels = len(self.pixels)
        off = (0, 0, 0)  # Replace with your desired 'off' color
        on = (255, 255, 255)  # Replace with your desired 'on' color

        i = 0
        j = i + window

        while j < num_pixels:
            self.pixels[i] = off
            self.pixels[j] = self.color_array[j]

            i+=1
            j+=1

            time.sleep(0.05)

    def stepstone(self):

        group_index = 0
        start_index = 0

        for led_group in self.led_groups:

            end_index = start_index + led_group

            section_size = self.led_groups[group_index]
            
            j = min(start_index + section_size, self.num_pixels)

            for brightness in range(256):
                section_brightness = tuple(
                    int(val * brightness / 255) for val in self.group_colors[group_index]
                )
                self.pixels[start_index:end_index] = [section_brightness] * (j - start_index)
                time.sleep(0.002)  # Adjust the sleep duration for a smoother transition

            start_index = end_index
            group_index += 1
        
        time.sleep(2)




