import array


class BaseEffect:
    def __init__(self, num_leds, bpp, **kwargs):
        self._updated = False
        self._num_leds = num_leds
        self.bpp = bpp
        self._kwargs = kwargs
        self._is_active = True

    @property
    def bpp(self):
        return self._bpp

    @bpp.setter
    def bpp(self, value):
        if value not in (3, 4):
            raise ValueError("Bpp must be eiher '3' or '4'")
        self._bpp = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a Boolean")
        self._is_active = value

    def _validate_color(self, color):
        if isinstance(color, tuple):
            if len(color) != self._bpp:
                raise ValueError(f"Color must be a tuple of length {self._bpp}")
            return color
        elif isinstance(color, list):
            for c in color:
                if not isinstance(c, tuple) or len(c) != self._bpp:
                    raise ValueError(
                        f"Each color in the list must be a tuple of length {self._bpp}"
                    )
            return color
        elif isinstance(color, bytearray) or isinstance(color, array.array):
            if len(color) % self._bpp != 0:
                raise ValueError(f"Bytearray length must be a multiple of {self._bpp}")
            return color
        else:
            raise ValueError(
                "Invalid color input. Must be a color tuple or a list of color tuples."
            )

    def is_updated(self):
        return self._updated

    def reset_update_flag(self):
        self._updated = False

    def update(self):
        raise NotImplementedError("This method must be overridden in subclasses")

    def get_colors(self):
        raise NotImplementedError("This method must be overridden in subclasses")
