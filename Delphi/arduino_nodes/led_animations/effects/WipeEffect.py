import time
import array
from .base_effect import BaseEffect


class WipeEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" not in kwargs:
            raise ValueError("Required argument 'color' is missing")
        self._wave_color = self._validate_color(kwargs.get("color"))

        self._speed = kwargs.get("speed", 1)
        self._reset_after_completion = kwargs.get("reset_after_completion", True)
        self._current_led = 0
        self._start_time = time.monotonic()
        self._off_color = (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)
        self._colors = [self._off_color] * num_leds

        self._colors = array.array("B", self._off_color * num_leds * bpp)

    def update(self):
        self._updated = True
        current_time = time.monotonic()

        if (
            current_time - self._start_time
        ) * self._speed >= 1 and self._current_led < self._num_leds:
            for j in range(self._bpp):
                self._colors[self._current_led * self._bpp + j] = self._wipe_color[j]
            self._current_led += 1
            self._start_time = current_time

            if self._current_led == self._num_leds and self._reset_after_completion:
                self._colors = array.array(
                    "B", self._off_color * self._num_leds * self._bpp
                )
                self._current_led = 0

    def get_colors(self):
        return self._colors
