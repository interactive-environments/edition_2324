import time
import array
from .base_effect import BaseEffect


class RainbowEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)
        self._duration = kwargs.get("duration", num_leds / 10)
        self._start_time = time.monotonic()

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    def update(self):
        self._updated = True
        elapsed_time = time.monotonic() - self._start_time
        progress = (elapsed_time % self._duration) / self._duration

        for i in range(self._num_leds):
            color = self._wheel(int(progress * 255 + i * 256 / self._num_leds) % 255)
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = color[j]

    def get_colors(self):
        return self._colors
