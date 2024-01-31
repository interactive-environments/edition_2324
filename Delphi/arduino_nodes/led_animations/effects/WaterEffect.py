import time
import math
import random
import array
from .base_effect import BaseEffect


class WaterEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        self._wave_length = kwargs.get("wave_length", 10)
        self._speed = kwargs.get("speed", 1)
        self._start_time = time.monotonic()
        self._base_colors = [
            self._generate_static_water_color() for _ in range(num_leds)
        ]

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _generate_static_water_color(self):
        blue_intensity = random.randint(0, 255)
        if self._bpp == 3:
            return (0, 0, blue_intensity)
        else:
            white_intensity = random.randint(0, 128)
            return (0, 0, blue_intensity, white_intensity)

    def _generate_wave_color(self, base_color, position, time_offset):
        wave = (
            math.sin(position / self._wave_length * 2 * math.pi + time_offset) + 1
        ) / 2
        intensity_modifier = int(128 * wave)
        return tuple(min(255, base + intensity_modifier) for base in base_color[:3])

    def update(self):
        self._updated = True
        current_time = time.monotonic()
        time_offset = (current_time - self._start_time) * self._speed

        for i in range(self._num_leds):
            base_color = self._base_colors[i]
            wave_color = self._generate_wave_color(base_color, i, time_offset)
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = wave_color[j]

    def get_colors(self):
        return self._colors
