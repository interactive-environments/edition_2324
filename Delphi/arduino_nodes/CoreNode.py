import board
import time
import neopixel
import config
from utils.enums import State

from led_animations.LEDController import LEDController

class CoreNode:
    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client

        if config.pixel_order == "rgbw":
            output_light = neopixel.NeoPixel(board.D2, config.output_led_num, auto_write=False, pixel_order=neopixel.RGBW)
        elif config.pixel_order == "rgb":
            output_light = neopixel.NeoPixel(board.D2, config.output_led_num, auto_write=False, pixel_order=neopixel.RGB)
        elif config.pixel_order == "grbw":
            output_light = neopixel.NeoPixel(board.D2, config.output_led_num, auto_write=False, pixel_order=neopixel.GRBW)
        elif config.pixel_order == "grb":
            output_light = neopixel.NeoPixel(board.D2, config.output_led_num, auto_write=False, pixel_order=neopixel.GRB)
        else:
            raise ValueError("Pixel order is not known")

        self._led_conroller = LEDController(output_light)
        self._state = None
        self._last_interaction = 0
        self.set_state('disconnected')

    @property
    def state(self):
        return self._state

    def reset(self):
        raise NotImplemented()

    def parse_message(self, client, topic, message):
        self._last_interaction = time.monotonic()
        project, system_id, event = topic.split("/")
        if system_id != config.system_id:
            raise ValueError(f"This node is not part of system: {system_id}")
        return system_id, event


    def set_state(self, value):
        print(f"Setting state: {value}")
        self._last_interaction = time.monotonic()
        if value not in [getattr(State, attr) for attr in dir(State) if not attr.startswith("__")]:
            raise ValueError(f"{value} is not a valid state")
        self._state = value

        if value == State.Inactive:
            self._led_conroller.set_effect('off')
        elif value == State.Disconnected:
            if self._led_conroller._bpp == 3:
                self._led_conroller.set_effect('strobe', color=(125, 125, 0), frequency=5)
            else:
                self._led_conroller.set_effect('strobe', color=(125, 125, 0, 0), frequency=5)
        elif value == State.Error:
            if self._led_conroller._bpp == 3:
                self._led_conroller.set_effect('strobe', color=(255, 0, 0), frequency=5)
            else:
                self._led_conroller.set_effect('strobe', color=(255, 0, 0, 0), frequency=5)

    def loop(self):
        if self.state != State.Idle and time.monotonic() - self._last_interaction > config.reset_threshold:
            self.reset()
        self._led_conroller.loop()
