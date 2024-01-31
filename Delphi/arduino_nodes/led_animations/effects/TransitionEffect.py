import time
import array
from led_animations import easing_functions as ease
from .base_effect import BaseEffect


class TransitionEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        start_color_input = kwargs.get("start_color") or kwargs.get("start_colors")
        self._start_colors = self._validate_color(
            self._process_color_input(start_color_input, num_leds)
        )

        end_color_input = kwargs.get("end_color") or kwargs.get("end_colors")
        self._end_colors = self._validate_color(
            self._process_color_input(end_color_input, num_leds)
        )

        self._steps = kwargs.get("steps", 30)
        self._duration = kwargs.get("duration", 3)
        self._step_duration = self._duration / self._steps

        easing = kwargs.get("easing_function", "LinearInOut")
        if not hasattr(ease, easing):
            raise ValueError(f"{easing} is not a valid easing function")
        self._easing_function = getattr(ease, easing)()

        self._current_step = 0
        self._start_time = time.monotonic()

        self._callback = kwargs.get("callback")
        self._callback_called = False

        self._colors = array.array("B", [color for color_tuple in self._start_colors for color in color_tuple])

    def _process_color_input(self, color_input, num_leds):
        if isinstance(color_input, tuple):
            return [color_input] * num_leds
        elif isinstance(color_input, list):
            if len(color_input) != num_leds:
                raise ValueError("Color list length must match number of LEDs")
            return color_input
        elif isinstance(color_input, (bytearray, array.array)):
            if len(color_input) != num_leds * self._bpp:
                raise ValueError("Bytearray length must be num_leds * bpp")
            return [
                tuple(color_input[i * self._bpp : (i + 1) * self._bpp])
                for i in range(num_leds)
            ]
        else:
            raise ValueError("Invalid color input type")

    def update(self):
        self._updated = True
        elapsed_time = time.monotonic() - self._start_time
        if elapsed_time < self._duration:
            progress = elapsed_time / self._duration
            eased_progress = self._easing_function(progress)
            self._interpolate_color(eased_progress)
        else:
            self._set_colors(self._end_colors)
            self.is_active = False
            if self._callback and not self._callback_called:
                self._callback_called = True
                self._callback()

    def _interpolate_color(self, eased_progress):
        for i in range(self._num_leds):
            start_color = self._start_colors[i]
            end_color = self._end_colors[i]
            interpolated_color = tuple(
                max(0, min(255, int(s + (e - s) * eased_progress)))
                for s, e in zip(start_color, end_color)
            )
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = interpolated_color[j]

    def _set_colors(self, colors):
        for i in range(self._num_leds):
            color = colors[i]
            for j in range(self._bpp):
                self._colors[i * self._bpp + j] = color[j]

    def get_colors(self):
        return self._colors
