import time
import math
import array
from .base_effect import BaseEffect


class BreatheEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" in kwargs:
            if "colors" in kwargs:
                raise ValueError("Effect cannot have both 'color' and 'colors' set")
            self._color_list = [self._validate_color(kwargs.get("color"))]
        elif "colors" in kwargs:
            self._color_list = self._validate_color(kwargs.get("colors"))
        else:
            raise ValueError("Required argument 'color' or 'colors' is missing")

        self._duration = kwargs.get("duration", 3)
        self._start_time = time.monotonic()
        self._color_index = 0

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _adjust_brightness(self, color, brightness_factor):
        return tuple(int(c * brightness_factor) for c in color)

    def update(self):
        self._updated = True
        elapsed_time = time.monotonic() - self._start_time
        total_cycle_time = self._duration * len(self._color_list)
        cycle_position = elapsed_time % total_cycle_time

        self._color_index = int(cycle_position // self._duration) % len(
            self._color_list
        )

        brightness_factor = (
            math.sin((cycle_position % self._duration) / self._duration * 2 * math.pi)
            + 1
        ) / 2
        current_color = self._color_list[self._color_index]

        for i in range(self._num_leds):
            adjusted_color = self._adjust_brightness(current_color, brightness_factor)
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = adjusted_color[j]

    def get_colors(self):
        return self._colors
