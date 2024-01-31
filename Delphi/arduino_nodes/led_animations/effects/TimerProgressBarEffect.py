import array
import time
from .base_effect import BaseEffect

class TimerProgressBarEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        self._color = self._validate_color(
            kwargs.get("color", (0, 255, 0) if bpp == 3 else (0, 255, 0, 0))
        )
        self._background_color = self._validate_color(
            kwargs.get("background_color", (0, 0, 0) if bpp == 3 else (0, 0, 0, 0))
        )

        self._reverse = kwargs.get("reverse", False)
        self._duration = kwargs.get("duration", 10)
        self._start_time = None
        self._colors = array.array(
            "B",
            [value for color in ([self._color] if self._reverse else [self._background_color]) * num_leds for value in color]
        )
        self._callback = kwargs.get("callback", None)
        self._timer_finished = False

        # Additional attributes for color transition
        self._target_color = self._color
        self._transition_steps = 30  # Number of steps for transition
        self._current_transition_step = 0

        self.start_timer()

    def start_timer(self):
        self._start_time = time.monotonic()
        self._timer_finished = False
        self._updated = True

    def set_new_color(self, new_color, transition_steps=30):
        self._target_color = self._validate_color(new_color)
        self._current_transition_step = 0
        self._transition_steps = transition_steps

    def _calculate_transition_color(self):
        if self._current_transition_step < self._transition_steps:
            transition_color = tuple(
                int(old + (new - old) * self._current_transition_step / self._transition_steps)
                for old, new in zip(self._color, self._target_color)
            )
            self._current_transition_step += 1
            return transition_color
        else:
            self._color = self._target_color
            return self._color

    def _calculate_progress(self):
        if self._start_time is None:
            return 0
        elapsed_time = time.monotonic() - self._start_time
        progress = (elapsed_time / self._duration) * 100
        return max(0, min(100, progress))

    def _apply_colors(self):
        progress = self._calculate_progress() / 100
        off_leds = int(progress * self._num_leds)
        fade_leds = 5

        def clamp(value):
            return max(0, min(255, int(value)))

        transition_color = self._calculate_transition_color()

        for i in range(self._num_leds):
            base_index = i * self._bpp

            if self._reverse:
                if i >= self._num_leds - off_leds - fade_leds:
                    if i < self._num_leds - off_leds:
                        fade_intensity = 1 - (self._num_leds - 1 - i - (self._num_leds - off_leds - fade_leds)) / fade_leds
                        color = tuple(clamp(c * fade_intensity) for c in transition_color)
                    else:
                        color = self._background_color
                else:
                    color = transition_color
            else:
                if i < off_leds:
                    color = transition_color
                elif i < off_leds + fade_leds:
                    fade_intensity = 1 - (i - off_leds) / fade_leds
                    color = tuple(clamp(c * fade_intensity) for c in transition_color)
                else:
                    color = self._background_color

            for j in range(self._bpp):
                self._colors[base_index + j] = clamp(color[j])

    def update(self):
        if not self._timer_finished:
            self._apply_colors()
            progress = self._calculate_progress()
            if progress >= 100:
                self._timer_finished = True
                if self._callback:
                    self._callback()
        self._updated = True

    def get_colors(self):
        return self._colors
