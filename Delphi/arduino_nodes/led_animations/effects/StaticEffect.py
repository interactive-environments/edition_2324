import array
from .base_effect import BaseEffect


class StaticEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)
        if "color" not in kwargs:
            raise ValueError("Required argument 'color' is missing")

        self._color = self._validate_color(kwargs["color"])

        if len(self._color) != bpp:
            raise ValueError(f"The color tuple length does not match bpp: {bpp}")

        self._colors = array.array(
            "B",
            [component for color in (self._color,) * num_leds for component in color],
        )
        self._updated = True

    def update(self):
        pass

    def get_colors(self):
        return self._colors
