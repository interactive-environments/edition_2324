import time
import array
import random
from .base_effect import BaseEffect


class SnakeEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        if "head_color" not in kwargs:
            raise ValueError("Required argument 'head_color' is missing")
        self._head_color = self._validate_color(kwargs.get("head_color"))

        if "body_color" not in kwargs:
            raise ValueError("Required argument 'body_color' is missing")
        self._body_color = self._validate_color(kwargs.get("body_color"))

        if "target_color" not in kwargs:
            raise ValueError("Required argument 'target_color' is missing")
        self._target_color = self._validate_color(kwargs.get("target_color"))

        self._initial_snake_length = kwargs.get("snake_length", 5)
        self._speed = kwargs.get("speed", 1)
        self._current_position = 0
        self._direction = 1
        self._off_color = (0, 0, 0) if bpp == 3 else (0, 0, 0, 0)
        self._colors = [self._off_color] * num_leds
        self._snake_length = self._initial_snake_length
        self._start_time = time.monotonic()
        self._target_position = self._place_new_target()

        self._colors = array.array("B", [0] * num_leds * bpp)
        self._off_color = [0] * bpp

    def _place_new_target(self):
        available_positions = set(range(self._num_leds)) - set(
            range(self._current_position, self._current_position + self._snake_length)
        )
        return random.choice(list(available_positions))

    def update(self):
        self._updated = True
        current_time = time.monotonic()
        if (current_time - self._start_time) * self._speed >= 1:
            self._current_position = (
                self._current_position + self._direction
            ) % self._num_leds
            self._start_time = current_time

            if self._current_position == self._target_position:
                self._snake_length += 1
                self._target_position = self._place_new_target()

            self._colors = array.array("B", self._off_color * self._num_leds)

            for i in range(self._snake_length):
                idx = (self._current_position + i) % self._num_leds
                color = (
                    self._body_color if i < self._snake_length - 1 else self._head_color
                )
                for j in range(self._bpp):
                    self._colors[idx * self._bpp + j] = color[j]

            for j in range(self._bpp):
                self._colors[
                    self._target_position * self._bpp + j
                ] = self._target_color[j]

    def get_colors(self):
        return self._colors
