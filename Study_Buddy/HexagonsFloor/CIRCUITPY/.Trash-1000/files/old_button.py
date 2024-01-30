# --- Imports
import digitalio
import time
import board

# --- Variables
button = digitalio.DigitalInOut(board.D7)
button.direction = digitalio.Direction.INPUT

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT
# --- Functions

# --- Setup

"""CircuitPython Essentials Internal RGB LED red, green, blue example"""
if hasattr(board, "APA102_SCK"):
    import adafruit_dotstar

    led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
else:
    import neopixel

    led = neopixel.NeoPixel(board.NEOPIXEL, 1)


led.brightness = 0.5

# --- Main loop
while True:
    if button.value == False:
        led[0] = (0, 0, 0)
    else:
        led[0] = (128, 0, 128)
