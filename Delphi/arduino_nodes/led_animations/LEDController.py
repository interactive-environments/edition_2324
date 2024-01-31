import array
import gc
import led_animations.effects as Effects


class LEDController:
    def __init__(self, neopixel):
        self._effect = None

        self._neopixel = neopixel
        self._leds = neopixel.n
        self._bpp = neopixel.bpp
        self._colors = array.array("B", [0] * self._leds * self._bpp)

    @property
    def effect(self):
        return self._effect

    def set_effect(self, name, **kwargs):
        gc.collect()
        if not hasattr(Effects, name):
            raise ValueError(f"Effect '{name}' does not exist")
        self._effect = getattr(Effects, name)(
            num_leds=self._leds, bpp=self._bpp, **kwargs
        )

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, value):
        if not isinstance(value, array.array) or len(value) != self._leds * self._bpp:
            raise ValueError("Invalid color array")

        # In-place update
        for i in range(0, len(value), self._bpp):
            update_needed = False
            for j in range(self._bpp):
                if self._colors[i + j] != value[i + j]:
                    self._colors[i + j] = value[i + j]
                    update_needed = True

            if update_needed:
                led_index = i // self._bpp
                self._neopixel[led_index] = tuple(self._colors[i : i + self._bpp])

        self._neopixel.show()

    def loop(self):
        if not self.effect:
            return

        if self.effect and self.effect.is_active:
            self.effect.update()
            if self.effect.is_updated():
                self.colors = self.effect.get_colors()
                self.effect.reset_update_flag()

        gc.collect()
