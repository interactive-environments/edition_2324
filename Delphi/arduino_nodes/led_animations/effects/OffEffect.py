import array
from .base_effect import BaseEffect


class OffEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        self._colors = array.array("B", [0] * num_leds * bpp)
        self._updated = True

    def update(self):
        pass

    def get_colors(self):
        return self._colors
