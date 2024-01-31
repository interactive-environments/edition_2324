import array
from .base_effect import BaseEffect

class ChaseEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "colors" not in kwargs:
            raise ValueError("Required argument 'colors' is missing")
        self._colors_list = self._validate_color(kwargs.get("colors"))

        self._speed = kwargs.get("speed", 5)
        self._current_position = 0
        self._colors = array.array("B", [0] * num_leds * bpp)

        # Calculate the size of each color segment
        self._segment_size = max(1, self._num_leds // len(self._colors_list))

    def update(self):
        self._updated = True
        self._current_position = (self._current_position + self._speed) % self._num_leds

        for i in range(self._num_leds):
            # Determine the color index based on the segment
            color_index = ((i + self._current_position) // self._segment_size) % len(self._colors_list)
            color = self._colors_list[color_index]

            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = color[j]

    def get_colors(self):
        return self._colors
