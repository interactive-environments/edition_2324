import array
from .base_effect import BaseEffect


class GradientEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "colors" not in kwargs:
            raise ValueError("Required argument 'colors' is missing")
        self._gradient_colors = self._validate_colors(kwargs.get("colors"))

        if len(self._gradient_colors) < 2:
            raise ValueError("Gradient effect requires at least two colors")

        self._colors = array.array("B", [0] * num_leds * bpp)
        self._create_gradient()
        self._updated = True

    def _create_gradient(self):
        segment_length = self._num_leds // (len(self._gradient_colors) - 1)
        position = 0

        for i in range(len(self._gradient_colors) - 1):
            start_color = self._gradient_colors[i]
            end_color = self._gradient_colors[i + 1]

            for j in range(segment_length):
                factor = j / segment_length
                interpolated_color = tuple(
                    int(start + factor * (end - start))
                    for start, end in zip(start_color, end_color)
                )

                for k in range(self._bpp):
                    self._colors[position * self._bpp + k] = interpolated_color[k]
                position += 1

        # Fill remaining LEDs with the last color
        while position < self._num_leds:
            for k in range(self._bpp):
                self._colors[position * self._bpp + k] = self._gradient_colors[-1][k]
            position += 1

    def update(self):
        pass

    def get_colors(self):
        return self._colors
