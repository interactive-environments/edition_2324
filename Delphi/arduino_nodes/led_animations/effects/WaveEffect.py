import time
import math
import array
from .base_effect import BaseEffect


class WaveEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" not in kwargs:
            raise ValueError("Required argument 'color' is missing")
        self._wave_color = self._validate_color(kwargs.get("color"))

        self._wave_length = kwargs.get("wave_length", 10)
        self._speed = kwargs.get("speed", 1)
        self._start_time = time.monotonic()

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _generate_wave_intensity(self, position, time_offset):
        wave_phase = position / self._wave_length * 2 * math.pi + time_offset
        intensity = (math.sin(wave_phase) + 1) / 2
        return intensity

    def update(self):
        self._updated = True
        current_time = time.monotonic()
        time_offset = (current_time - self._start_time) * self._speed

        for i in range(self._num_leds):
            intensity = self._generate_wave_intensity(i, time_offset)
            wave_color = tuple(int(c * intensity) for c in self._wave_color)

            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = wave_color[j]

    def get_colors(self):
        return self._colors
