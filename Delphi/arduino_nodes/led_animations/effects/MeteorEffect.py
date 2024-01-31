import time
import random
import array
from .base_effect import BaseEffect


class MeteorEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" in kwargs:
            if "colors" in kwargs:
                raise ValueError("Effect cannot have both 'color' and 'colors' set")
            self._color_list = [self._validate_color(kwargs.get("color"))]
        elif "colors" in kwargs:
            self._color_list = self._validate_color(kwargs.get("colors"))
        else:
            raise ValueError("Required argument 'color' or 'colors' is missing")

        self._meteor_size = kwargs.get("meteor_size", 5)
        self._tail_length = kwargs.get("tail_length", 10)
        self._speed = kwargs.get("speed", 1)
        self._start_time = time.monotonic()
        self._spawn_chance = kwargs.get("spawn_chance", 0.01)
        self._meteors = []
        self._off_color = (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _spawn_meteor(self):
        if random.random() < self._spawn_chance:
            self._meteors.append(
                {
                    "position": 0 - self._meteor_size,
                    "color": random.choice(self._color_list),
                }
            )

    def update(self):
        self._updated = True
        self._spawn_meteor()

        for meteor in self._meteors:
            meteor["position"] += self._speed

        self._meteors = [
            m
            for m in self._meteors
            if m["position"] - self._tail_length < self._num_leds
        ]

        self._colors = array.array("B", [0] * self._num_leds * self._bpp)

        for meteor in self._meteors:
            for i in range(self._num_leds):
                if meteor["position"] - self._tail_length <= i < meteor["position"]:
                    intensity = (
                        i - meteor["position"] + self._tail_length
                    ) / self._tail_length
                    new_color = tuple(int(c * intensity) for c in meteor["color"])

                    for j in range(self._bpp):
                        color_index = i * self._bpp + j
                        self._colors[color_index] = min(
                            255, self._colors[color_index] + new_color[j]
                        )

    def get_colors(self):
        return self._colors
