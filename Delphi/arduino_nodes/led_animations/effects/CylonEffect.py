import time
import array
from .base_effect import BaseEffect


class CylonEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" not in kwargs:
            raise ValueError("Required argument 'color' is missing")
        self._color = self._validate_color(kwargs.get("color"))

        self._tail_length = kwargs.get("tail_length", 3)
        self._speed = kwargs.get("speed", 1)
        self._current_position = 0
        self._direction = 1
        self._start_time = time.monotonic()

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _calculate_tail_intensity(self, distance):
        if distance <= self._tail_length:
            return max(0, (self._tail_length - distance) / self._tail_length)
        return 0

    def update(self):
        self._updated = True
        self._current_position += self._speed * self._direction

        if self._current_position >= self._num_leds - 1 or self._current_position <= 0:
            self._direction *= -1

        for i in range(self._num_leds):
            distance = abs(i - self._current_position)
            intensity = self._calculate_tail_intensity(distance)
            color = tuple(int(c * intensity) for c in self._color)

            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = color[j]

    def get_colors(self):
        return self._colors
