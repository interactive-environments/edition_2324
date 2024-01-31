import time
import array
from .base_effect import BaseEffect


class ShiftEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "colors" not in kwargs:
            raise ValueError("Effect cannot have both 'colors' set")
        self._input_colors = self._validate_color(kwargs.get("colors"), num_leds)

        self._shift_direction = kwargs.get("shift_direction", "right")
        if self._shift_direction not in ("left", "right"):
            raise ValueError("Shift direction must be either 'left' or 'right'")

        self._speed = kwargs.get("speed", 1)
        self._start_time = time.monotonic()

        self._colors = array.array("B", [0] * num_leds * bpp)
        self._set_initial_colors()

    def _set_initial_colors(self):
        for i in range(self._num_leds):
            color = self._input_colors[i]
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = color[j]

    def update(self):
        self._updated = True
        current_time = time.monotonic()
        if (current_time - self._start_time) * self._speed >= 1:
            if self._shift_direction == "right":
                self._colors = self._colors[-self._bpp :] + self._colors[: -self._bpp]
            elif self._shift_direction == "left":
                self._colors = self._colors[self._bpp :] + self._colors[: self._bpp]
            self._start_time = current_time

    def get_colors(self):
        return self._colors
