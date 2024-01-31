import time
import array
from .base_effect import BaseEffect


class StrobeEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" not in kwargs:
            raise ValueError("Required argument 'color' is missing")
        self._strobe_color = self._validate_color(kwargs.get("color"))

        self._frequency = kwargs.get("frequency", 1)
        self._start_time = time.monotonic()
        self._state_on = True
        self._off_color = (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)

        self._colors = array.array("B", [0] * num_leds * bpp)

    def update(self):
        self._updated = True
        current_time = time.monotonic()
        elapsed_time = current_time - self._start_time

        period = 1 / self._frequency
        if elapsed_time >= period:
            self._state_on = not self._state_on
            self._start_time = current_time - (elapsed_time % period)

        color_to_use = self._strobe_color if self._state_on else self._off_color
        for i in range(self._num_leds):
            start_index = i * self._bpp
            end_index = start_index + self._bpp
            self._colors[start_index:end_index] = array.array("B", color_to_use)

    def get_colors(self):
        return self._colors
