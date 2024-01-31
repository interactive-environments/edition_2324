import time
import random
import array
from .base_effect import BaseEffect


class TwinkleEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "color" in kwargs:
            if "colors" in kwargs:
                raise ValueError("Effect cannot have both 'color' and 'colors' set")
            self._twinkle_colors = [self._validate_color(kwargs.get("color"))]
        elif "colors" in kwargs:
            self._twinkle_colors = self._validate_color(kwargs.get("colors"))
        else:
            raise ValueError("Required argument 'color' or 'colors' is missing")

        self._twinkle_chance = kwargs.get("twinkle_chance", 0.05)
        self._duration = kwargs.get("duration", 0.5)
        self._fade_duration = kwargs.get("fade_duration", 0.5)
        self._fallback_color = kwargs.get(
            "off_color", (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)
        )
        self._colors = [self._fallback_color] * num_leds
        self._twinkle_states = [
            {"end_time": 0, "fade_end_time": 0, "color": self._fallback_color}
            for _ in range(num_leds)
        ]

        self._colors = array.array("B", [0] * num_leds * bpp)

    def _fade_color(self, start_color, end_color, progress):
        return tuple(
            int(start + (end - start) * progress)
            for start, end in zip(start_color, end_color)
        )

    def update(self):
        self._updated = True
        current_time = time.monotonic()

        for i in range(self._num_leds):
            state = self._twinkle_states[i]
            if current_time > state["fade_end_time"]:
                if random.random() < self._twinkle_chance:
                    state["color"] = random.choice(self._twinkle_colors)
                    state["end_time"] = current_time + self._duration
                    state["fade_end_time"] = state["end_time"] + self._fade_duration
                else:
                    state["color"] = self._fallback_color

            elif current_time > state["end_time"]:
                progress = (current_time - state["end_time"]) / self._fade_duration
                state["color"] = self._fade_color(
                    state["color"], self._fallback_color, progress
                )

            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = state["color"][j]

    def get_colors(self):
        return self._colors
