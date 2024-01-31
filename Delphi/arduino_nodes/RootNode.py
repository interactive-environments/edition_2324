import time
import random
import json
import traceback
import config
from CoreNode import CoreNode
from utils.enums import State
from utils.color import blend_colors, rgb_to_hex
from led_animations.Effects.TimerProgressBarEffect import TimerProgressBarEffect


HSL_RANGES = [
    # Autumn: Greens, yellows, oranges, reds
    {"theme": "Autumn", "h": [(20, 120)], "s": [(50, 100)], "l": [(30, 60)]},
    # Ocean: Blues, teals, and a hint of green
    {"theme": "Ocean", "h": [(150, 250)], "s": [(50, 100)], "l": [(30, 60)]},
    # Sunset: Oranges, reds, purples, pinks, and some blues
    {"theme": "Sunset", "h": [(0, 80), (240, 360)], "s": [(60, 100)], "l": [(30, 70)]},
    # Forest: Variety of greens with touches of yellow and blue
    {"theme": "Forest", "h": [(60, 160)], "s": [(40, 80)], "l": [(20, 60)]},
    # Tropical: Blues, greens, yellows, reds, and purples
    {"theme": "Tropical", "h": [(50, 200)], "s": [(60, 100)], "l": [(30, 70)]},
    # Winter: Cool blues, purples, pale greens, and hints of pink
    {"theme": "Winter", "h": [(170, 300)], "s": [(30, 80)], "l": [(20, 60)]},
    # Pastel: Soft hues across the spectrum
    {"theme": "Pastel", "h": [(0, 360)], "s": [(20, 60)], "l": [(30, 70)]},
    {"theme": "Pastel", "h": [(0, 360)], "s": [(20, 60)], "l": [(30, 70)]},
    {"theme": "Pastel", "h": [(0, 360)], "s": [(20, 60)], "l": [(30, 70)]},
    {"theme": "Pastel", "h": [(0, 360)], "s": [(20, 60)], "l": [(30, 70)]},
    {"theme": "Pastel", "h": [(0, 360)], "s": [(20, 60)], "l": [(30, 70)]},
    # Desert: Earthy oranges, reds, browns, and muted yellows
    {"theme": "Desert", "h": [(15, 90)], "s": [(40, 70)], "l": [(30, 60)]},
    # Sunrise: Reds, oranges, yellows, pinks, and hints of purple
    {"theme": "Sunrise", "h": [(0, 100)], "s": [(70, 100)], "l": [(30, 60)]},
]


class RootNode(CoreNode):
    def __init__(self, mqtt_client):
        super().__init__(mqtt_client)

        self._active = False
        self._active_last_update = 0
        self._elapsed_time = 0
        self._transitioning = False
        self._updated = False
        self._system_data = {}
        self._blended_color = (0, 0, 0)

    def reset(self):
        self._active = False
        self._active_last_update = 0
        self._elapsed_time = 0
        self._transitioning = False
        self._updated = False
        self._system_data = {}
        self._blended_color = (0, 0, 0)
        self.generate_seed()
        self.mqtt.publish(f"{config.mqtt_prepend}/state", "idle", retain=True)

    def generate_seed(self):
        seed = int(time.monotonic())
        hsl_range = random.choice(HSL_RANGES)
        self.mqtt.publish(
            f"{config.mqtt_prepend}/color_seed",
            json.dumps(
                {
                    "seed": seed,
                    "h": hsl_range["h"],
                    "s": hsl_range["s"],
                    "l": hsl_range["l"],
                }
            ),
            retain=True,
        )

    def _end_interaction(self):
        if not self._active:
            return
        self._active = False
        package = {
            "color": rgb_to_hex(
                self._blended_color[0], self._blended_color[1], self._blended_color[2]
            ),
            "location": config.location,
            "ISO_location": config.ISO_location,
        }

        counter = 0
        while counter < 6:
            try:
                self.mqtt.publish(
                    f"{config.mqtt_prepend}/system_data", json.dumps(package)
                )
                self.mqtt.publish(
                    f"{config.mqtt_prepend}/state", "prompting", retain=True
                )
                break
            except Exception as e:
                print(e)
                time.sleep(2)
                counter += 1

    def _end_transition(self, set_timer=False):
        self._transitioning = False
        if set_timer:
            self._led_conroller.set_effect(
                "timer",
                color=self._blended_color,
                reverse=True,
                duration=config.interaction_end_threshold,
                callback=lambda: self._end_interaction(),
            ),

    def _randomize_color(self):
        random_rgb = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self._transitioning = True
        self._led_conroller.set_effect(
            "transition",
            start_colors=self._led_conroller.colors,
            end_colors=random_rgb,
            steps=50,
            duration=5,
            callback=lambda: self._end_transition(),
        )

        if self.mqtt.is_connected():
            try:
                self.mqtt.publish(
                    f"{config.mqtt_prepend}/root_color",
                    json.dumps({"color": random_rgb, "duration": 5}),
                    retain=True,
                )
            except Exception as e:
                print(e)

    def _calculate_color(self):
        colors = {}
        for key in self._system_data:
            colors[self._system_data[key]["color"]] = self._system_data[key][
                "intensity"
            ]
        self._blended_color = blend_colors(colors)
        if (
            isinstance(self._led_conroller._effect, TimerProgressBarEffect)
            and time.monotonic() - self._led_conroller._effect._start_time
            < 0.5 * config.interaction_end_threshold
        ):
            self._led_conroller._effect.set_new_color(self._blended_color, 30)
        else:
            self._transitioning = True
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_color=self._blended_color,
                steps=10,
                duration=1,
                callback=lambda: self._end_transition(set_timer=True),
            )
        self._updated = False

        if self.mqtt.is_connected():
            try:
                self.mqtt.publish(
                    f"{config.mqtt_prepend}/root_color",
                    json.dumps({"color": self._blended_color, "duration": 1}),
                    retain=True,
                )
            except Exception as e:
                print(e)

    def parse_message(self, client, topic, message):
        try:
            system_id, event = super().parse_message(client, topic, message)
            if event == "state":
                self.set_state(message)
            elif event == "reset":
                self.reset()
            elif event == "input_data":
                try:
                    parsed_message = json.loads(message)
                except Exception as e:
                    print("JSON decode error:", e)
                    return
                if self.state == State.Idle:
                    self.set_state("active")
                elif self.state != State.Active:
                    return
                if parsed_message["id"] in self._system_data:
                    self._elapsed_time += (
                        parsed_message["interaction_time"]
                        - self._system_data[parsed_message["id"]]["interaction_time"]
                    )
                else:
                    self._elapsed_time += parsed_message["interaction_time"]
                self._system_data[parsed_message["id"]] = parsed_message
                self._active_last_update = time.monotonic()
                self._updated = True
            elif event == "image_sent":
                if message in ["true", "True"] and self.state != State.Printing:
                    self.mqtt.publish(
                        f"{config.mqtt_prepend}/state", "printing", retain=True
                    )
                    self.set_state(State.Printing)
                else:
                    raise ValueError("Image was not able to be sent")
            else:
                raise ValueError("Unkown or unimplemented event in message handler")
        except Exception as e:
            traceback.print_exception(e)
            print("Error parsing message:", e)
            self.mqtt.publish(f"{config.mqtt_prepend}/state", "error", retain=True)

    def set_state(self, value):
        super().set_state(value)

        if value == State.Active:
            self._active = True
            self._active_last_update = time.monotonic()
            self._transitioning = True
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_colors=(0, 0, 0),
                steps=10,
                duration=1,
                callback=lambda: self._end_transition(),
            )
        elif value == State.Idle:
            self._active = False
            self._transitioning = True
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_colors=(0, 0, 0),
                steps=10,
                duration=1,
                callback=lambda: self._end_transition(),
            )
        elif value == State.Prompting:
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_colors=(0, 0, 0),
                steps=20,
                duration=2,
                callback=lambda: self._led_conroller.set_effect(
                    "twinkle",
                    colors=[
                        (153, 0, 204),
                        (191, 0, 255),
                        (204, 51, 255),
                        (217, 102, 255),
                        (230, 153, 255),
                    ],
                ),
            )
        elif value == State.Printing:
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_colors=(0, 0, 0),
                steps=20,
                duration=2,
                callback=lambda: self._led_conroller.set_effect(
                    "chase",
                    speed=1,
                    colors=[
                        (0, 255, 255),
                        (255, 0, 255),
                        (255, 255, 0),
                        (0, 0, 0),
                    ],
                ),
            )

    def loop(self):
        if (
            self.state != State.Idle
            and time.monotonic() - self._last_interaction > config.reset_threshold
        ):
            self.mqtt.publish(f"{config.mqtt_prepend}/reset", "true")
            self._last_interaction = time.monotonic()
        super().loop()
        if self.state == State.Active:
            if self._active and self._updated and not self._transitioning:
                self._calculate_color()
        elif self.state == State.Idle:
            if not self._active and not self._transitioning:
                self._randomize_color()
