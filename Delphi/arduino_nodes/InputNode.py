import time
import board
import busio
import json
import random
import config
import adafruit_mpr121
from CoreNode import CoreNode
from utils.enums import State
from utils.color import darken, rgb_to_hex, hsl_to_rgb


class InputNode(CoreNode):
    def __init__(self, mqtt_client):
        super().__init__(mqtt_client)
        self.color = config.color
        self.rgb_color = config.rgb_color

        i2c = busio.I2C(board.SCL, board.SDA)
        self._touch_sensor = adafruit_mpr121.MPR121(i2c)
        self._touch_calibration_points = config.touch_sensor_calibration_points
        self._touch_calibration_buffer = [0] * self._touch_calibration_points
        self._touch_calibration_skips = config.touch_calibration_skips
        self._touch_calibration_avg = 0
        self._touch_calibration_index = 0
        self._touch_threshold = config.touch_sensor_threshold
        self._buffered_state = None
        self._touch_count = 0
        self._touch_count_threshold = config.touch_sensor_count_threshold

        self.data = {
            "id": config.device_id,
            "color": config.color,
            "interaction_count": 0,
            "interaction_time": 0.0,
            "intensity": 0,
        }

        self._updated = False
        self._intensity = 0
        self._interaction_count = 0
        self._interaction_time = 0.0
        self._start_touch_time = 0.0
        self._end_touch_time = 0.0
        self._touch_active = False

        self._last_update = 0.0
        self._start_calibration()

    def _start_calibration(self):
        self._buffered_state = self.state
        self._calibrating = True

    def _is_color_unique(self, new_color, existing_colors, threshold=15):
        for color in existing_colors:
            if abs(color[0] - new_color[0]) < threshold:
                return False
        return True

    def _select_random_range(self, ranges):
        return random.choice(ranges)

    def _generate_color(self, seed, hue_ranges, saturation_ranges, lightness_ranges):
        random.seed(seed)
        colors = []

        while len(colors) < config.device_id:
            hue_range = self._select_random_range(hue_ranges)
            saturation_range = self._select_random_range(saturation_ranges)
            lightness_range = self._select_random_range(lightness_ranges)

            hue = random.uniform(*hue_range)
            saturation = random.uniform(*saturation_range) / 100
            lightness = random.uniform(*lightness_range) / 100
            new_color = (hue, saturation, lightness)
            if self._is_color_unique(new_color, colors):
                colors.append(new_color)
        self.rgb_color = hsl_to_rgb(*colors[config.device_id - 1])
        self.color = rgb_to_hex(*self.rgb_color)

    def _calibrate_sensor(self):
        if self._touch_calibration_index < self._touch_calibration_skips:
            self._touch_sensor.baseline_data(0)
            self._touch_calibration_index += 1
            return

        self._touch_calibration_buffer[
            self._touch_calibration_index - self._touch_calibration_skips
        ] = self._touch_sensor.baseline_data(0)
        self._touch_calibration_index += 1
        if (
            self._touch_calibration_index - self._touch_calibration_skips
            >= self._touch_calibration_points
        ):
            self._touch_calibration_avg = (
                sum(self._touch_calibration_buffer) / self._touch_calibration_points
            )
            self._calibrating = False
            self._touch_calibration_index = 0
            if self._buffered_state is not None:
                self.set_state(self._buffered_state)
            else:
                self._state = None
            self._buffered_state = None

    def _sensor_touched(self):
        diff = abs(self._touch_calibration_avg - self._touch_sensor.baseline_data(0))
        return diff > self._touch_threshold

    def _gather_input(self):
        if self._sensor_touched():
            if not self._touch_active:
                self._touch_count += 1

                if self._touch_count > self._touch_count_threshold:
                    self._touch_count = self._touch_count_threshold
                    self._touch_active = True
                    self._interaction_count += 1
                    self._start_touch_time = time.monotonic()
                    self.set_state(State.Active)
                    self._updated = True
                    if self._intensity < 100:
                        # self._intensity += 1 * config.intensity_growth
                        self._intensity = 100
                    else:
                        self._intensity = 0
        else:
            if self._touch_count > 0:
                self._touch_count -= 1
            if self._touch_active and self._touch_count <= 0:
                self._touch_count = 0
                self._touch_active = False
                self._interaction_time += time.monotonic() - self._start_touch_time
                self._end_touch_time = time.monotonic()
                self.set_state(State.Idle)
                self._updated = True
            """
            if (
                self._intensity > 0
                and time.monotonic() - self._end_touch_time
                > config.intensity_falloff_start
            ):
                self._intensity -= 1 * config.intensity_falloff_factor
                self._updated = True
            """
        self._intensity = min(max(self._intensity, 0), 100)
        if (
            self.mqtt.is_connected()
            and time.monotonic() - self._last_update > 1 / config.sups
        ):
            try:
                package = {
                    "id": config.device_id,
                    "color": self.color,
                    "interaction_count": self._interaction_count,
                    "interaction_time": self._interaction_time,
                    "intensity": self._intensity,
                }

                if self._updated:
                    self._updated = False
                    self.data = package
                    self.mqtt.publish(
                        f"{config.mqtt_prepend}/input_data", json.dumps(self.data)
                    )
                self._last_update = time.monotonic()
            except Exception as e:
                print(e)

    def reset(self):
        self._intensity = 0
        self._interaction_count = 0
        self._interaction_time = 0.0
        self._start_touch_time = 0.0
        self._end_touch_time = 0.0
        self._touch_active = False
        self.set_state("idle")
        self.data = {
            "id": config.device_id,
            "color": self.color,
            "interaction_count": 0,
            "interaction_time": 0.0,
            "intensity": 0,
        }

        self._touch_calibration_buffer = [0] * self._touch_calibration_points
        self._touch_calibration_avg = 0
        self._touch_calibration_index = 0
        self._buffered_state = None
        self._start_calibration()

    def parse_message(self, client, topic, message):
        try:
            system_id, event = super().parse_message(client, topic, message)
            if event == "state":
                if self._calibrating:
                    self._buffered_state = message
                else:
                    self.set_state(message)
            elif event == "color_seed":
                try:
                    parsed_message = json.loads(message)
                except Exception as e:
                    print("JSON decode error:", e)
                    return
                self._generate_color(
                    parsed_message['seed'],
                    parsed_message['h'],
                    parsed_message['s'],
                    parsed_message['l'],
                )
            elif event == "reset":
                self.reset()
            else:
                raise ValueError("Unkown or unimplemented event in message handler")
        except Exception as e:
            print("Error parsing message:", e)
            self.mqtt.publish(f"{config.mqtt_prepend}/state", "error", retain=True)

    def set_state(self, value):
        super().set_state(value)

        if value == State.Active:
            self._led_conroller.set_effect("static", color=(self.rgb_color) + (0,))
        elif value == State.Idle:
            if self._intensity != 0:
                factor = min(max(1 - (100 / self._intensity), 0), 0.9)
                chance = 0.15
            else:
                factor = 0.9
                chance = 0.05

            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_color=(0, 0, 0, 0),
                steps=10,
                duration=1,
                callback=lambda: self._led_conroller.set_effect(
                    "twinkle",
                    twinkle_chance=chance,
                    colors=[
                        (darken(self.rgb_color, factor) + (0,)),
                    ],
                ),
            )
        elif value == State.Prompting:
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_color=(204, 51, 255, 0),
                steps=20,
                duration=2,
                callback=lambda: self._led_conroller.set_effect(
                    "twinkle",
                    colors=[
                        (153, 0, 204, 0),
                        (191, 0, 255, 0),
                        (204, 51, 255, 0),
                        (217, 102, 255, 0),
                        (230, 153, 255, 0),
                    ],
                ),
            )
        elif value == State.Printing:
            self._led_conroller.set_effect(
                "transition",
                start_colors=self._led_conroller.colors,
                end_color=(255, 255, 255, 0),
                steps=20,
                duration=2,
                callback=lambda: self._led_conroller.set_effect(
                    "twinkle",
                    colors=[
                        (230, 255, 230, 0),
                        (230, 255, 255, 0),
                        (255, 255, 230, 0),
                        (255, 255, 255, 0),
                        (230, 230, 255, 0),
                        (255, 230, 255, 0),
                        (255, 230, 230, 0),
                    ],
                ),
            )
        elif value == State.Calibrating:
            self._led_conroller.set_effect(
                "strobe", color=(125, 0, 125, 0), frequency=5
            )

    def loop(self):
        super().loop()
        if self._calibrating:
            if self._touch_calibration_index == 0:
                self.set_state(State.Calibrating)
            self._calibrate_sensor()
        if self.state == State.Active:
            self._gather_input()
        elif self.state == State.Idle:
            self._gather_input()
