# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Internal RGB LED red, green, blue example"""
import time
import board

if hasattr(board, "APA102_SCK"):
    import adafruit_dotstar

    led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    import neopixel

    led = neopixel.NeoPixel(board.NEOPIXEL, 1)

led.brightness = 0.3

color = [0, 0, 0]

increment = 6

while True:
    if color[0] <= 0:
        color[0] = 0
        color[1] = 0
        color[2] = 0
        increment = 6

    if color[0] >= 50:
        color[0] = 50
        color[1] = 50
        color[2] = 50
        increment = -6

    led[0] = (color[0], color[1], color[2])
    time.sleep(0.1)

    color[0] += increment
    color[1] += increment
