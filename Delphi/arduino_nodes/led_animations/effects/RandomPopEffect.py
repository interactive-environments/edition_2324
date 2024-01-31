import time
import random
import array
from .base_effect import BaseEffect


class RandomPopEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" in kwargs:
            if "colors" in kwargs:
                raise ValueError("Effect cannot have both 'color' and 'colors' set")
            self._colors_list = [self._validate_color(kwargs["color"])]
        elif "colors" in kwargs:
            self._colors_list = self._validate_color(kwargs["colors"])
        else:
            raise ValueError("Required argument 'color' or 'colors' is missing")

        self._pop_chance = kwargs.get("pop_chance", 0.1)
        self._pop_duration = kwargs.get("pop_duration", 0.5)
        self._popped_leds = {}
        self._off_color = (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)

        self._colors = array.array("B", [0] * num_leds * bpp)

    def update(self):
        self._updated = True
        current_time = time.monotonic()

        for i in range(self._num_leds):
            if random.random() < self._pop_chance and i not in self._popped_leds:
                self._popped_leds[i] = current_time + self._pop_duration
                color = random.choice(self._colors_list)
                for j in range(self._bpp):
                    self._colors[i * self._bpp + j] = color[j]
            elif i in self._popped_leds and self._popped_leds[i] < current_time:
                del self._popped_leds[i]
                for j in range(self._bpp):
                    self._colors[i * self._bpp + j] = self._off_color[j]
            elif i not in self._popped_leds:
                for j in range(self._bpp):
                    self._colors[i * self._bpp + j] = self._off_color[j]

    def get_colors(self):
        return self._colors
