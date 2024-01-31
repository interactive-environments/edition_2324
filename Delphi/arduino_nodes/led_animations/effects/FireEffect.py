import random
import array
from .base_effect import BaseEffect


class FireEffect(BaseEffect):
    def __init__(self, num_leds, bpp, **kwargs):
        super().__init__(num_leds, bpp, **kwargs)

        self._fire_color = self._validate_color(
            kwargs.get("fire_color", (255, 85, 0) if bpp == 3 else (255, 85, 0, 0))
        )
        base_color = self._validate_color(
            kwargs.get("base_color", (45, 0, 0) if bpp == 3 else (45, 0, 0, 0))
        )
        self._base_color = array.array("B", base_color * num_leds)

        self._colors = array.array("B", [0] * num_leds * bpp)
        self._cooling = kwargs.get("cooling", 120)
        self._sparking = kwargs.get("sparking", 120)
        self._intensity_variation_range = kwargs.get("intensity_variation_range", 10)
        self._heat = [0] * num_leds

    def _fire_spark(self):
        # Cool down every cell a little
        for i in range(self._num_leds):
            self._heat[i] = max(
                0,
                self._heat[i]
                - random.randint(0, ((self._cooling * 10) // self._num_leds) + 2),
            )

        # Randomly ignite new sparks at random positions
        if random.randint(0, 255) < self._sparking:
            spark_position = random.randint(0, self._num_leds - 1)
            spark_heat = min(
                255, random.randint(160, 255) * random.uniform(0.8, 1.2)
            )  # Varying intensity

            # Update the heat of the spark position and spread to a wider range
            spread_range = 3  # Number of cells on each side affected by the spark
            for i in range(
                max(0, spark_position - spread_range),
                min(self._num_leds, spark_position + spread_range + 1),
            ):
                distance = abs(spark_position - i)
                heat_factor = (spread_range - distance + 1) / (spread_range + 1)
                self._heat[i] = min(255, self._heat[i] + int(spark_heat * heat_factor))

    def _heat_to_color(self, temperature, base_index):
        t = min(temperature, 255) / 255
        red_index = base_index
        green_index = base_index + 1
        blue_index = base_index + 2

        base_red = self._base_color[red_index]
        base_green = self._base_color[green_index]
        base_blue = self._base_color[blue_index]

        if self._bpp == 3:
            new_red = int(base_red + (self._fire_color[0] - base_red) * t)
            new_green = int(base_green + (self._fire_color[1] - base_green) * t)
            new_blue = int(base_blue + (self._fire_color[2] - base_blue) * t)
            return (new_red, new_green, new_blue)
        else:
            new_red = int(base_red + (self._fire_color[0] - base_red) * t)
            new_green = int(base_green + (self._fire_color[1] - base_green) * t)
            new_blue = int(base_blue + (self._fire_color[2] - base_blue) * t)
            return (new_red, new_green, new_blue, 0)

    def _update_base_color(self):
        for i in range(0, len(self._base_color), 3):
            intensity_variation = random.randint(
                -self._intensity_variation_range, self._intensity_variation_range
            )
            new_red = max(0, min(255, self._base_color[i] + intensity_variation))
            self._base_color[i] = new_red

    def update(self):
        self._updated = True
        self._fire_spark()
        self._update_base_color()
        for i in range(self._num_leds):
            base_index = i * self._bpp
            color = self._heat_to_color(self._heat[i], base_index)
            self._colors[base_index : base_index + self._bpp] = array.array("B", color)

    def get_colors(self):
        return self._colors
