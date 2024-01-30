import os
import time
import board
import analogio
import digitalio
import neopixel
from wifiController import WifiController

# Set updates per second
UPS = 100

# Setup environment variables
NODE_NAME = os.getenv('name')
NODE_ID = os.getenv('id')
NODE_SYSTEM_ID = os.getenv('system_id')
NODE_COLOR = os.getenv('color')
OUTPUT_LED_LEDS = os.getenv('output_led_leds')
OUTPUT_LED_PIXEL_ORDER = getattr(neopixel, os.getenv('output_led_order'))
INTENSITY_DELTA = os.getenv('intensity_delta')

# Setup RGB and RGBW colors
BASE_COLOR_RGB = tuple(int(NODE_COLOR.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
BASE_COLOR_RGBW = BASE_COLOR_RGB + (0,)

# Setup board LED
BOARD_LED = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0, auto_write=True, pixel_order=neopixel.GRB)
BOARD_LED.fill(BASE_COLOR_RGB)
BOARD_LED.show()

# Setup output LED
OUTPUT_LED_PIN = board.D13
OUTPUT_LED_HAS_WHITE = True if OUTPUT_LED_PIXEL_ORDER == neopixel.GRBW or OUTPUT_LED_PIXEL_ORDER == neopixel.RGBW else False
OUTPUT_LED = neopixel.NeoPixel(OUTPUT_LED_PIN, OUTPUT_LED_LEDS, brightness=1.0, auto_write=True, pixel_order=OUTPUT_LED_PIXEL_ORDER)
OUTPUT_LED.fill(BASE_COLOR_RGBW) if OUTPUT_LED_HAS_WHITE else OUTPUT_LED.fill(BASE_COLOR_RGB)
OUTPUT_LED.show()

# Setup inputs
INPUT_1_PIN = board.D7
INPUT_2_PIN = board.D4
INPUT_1 = digitalio.DigitalInOut(INPUT_1_PIN)
INPUT_2 = digitalio.DigitalInOut(INPUT_2_PIN)
INPUT_1.direction = digitalio.Direction.INPUT
INPUT_2.direction = digitalio.Direction.INPUT

# Starting intensity
intensity = 100
# Current color
color_rgb = BASE_COLOR_RGB
color_rgbw = BASE_COLOR_RGB + (0,)

wifiController = WifiController(BOARD_LED, BASE_COLOR_RGB)

while True:
    now = time.monotonic()
    wifiController.checkConnection(now)

    if (INPUT_1.value):
        intensity += INTENSITY_DELTA
        intensity = min(100, intensity)
    if (INPUT_2.value):
        intensity -= INTENSITY_DELTA
        intensity = max(0, intensity)
    color_rgb = (
        int(BASE_COLOR_RGB[0] * intensity / 100),
        int(BASE_COLOR_RGB[1] * intensity / 100),
        int(BASE_COLOR_RGB[2] * intensity / 100),
    )
    color_rgbw = color_rgb + (0,)

    OUTPUT_LED.fill(color_rgbw) if OUTPUT_LED_HAS_WHITE else OUTPUT_LED.fill(color_rgb)
    HEX_COLOR = '#{:02x}{:02x}{:02x}'.format(color_rgb[0], color_rgb[1], color_rgb[2])
    time.sleep(1 / UPS)
