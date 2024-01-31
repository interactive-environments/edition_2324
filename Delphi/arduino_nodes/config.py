from utils.SimpleNamespace import SimpleNamespace
from utils.enums import Environment, NodeType
from utils.color import hex_to_rgb

version = "1.16"
project_name = "DELPHI"

"""Base device settings"""
device_id = 2
system_id = "system_1"

node_type = NodeType.Root  # The type of this node, choose an available class
color = "#000FFF"  # Base color for the output LEDs
rgb_color = hex_to_rgb(color)
output_led_num = 138  # Number of output LEDs
pixel_order = "grb"  # LED pixel order
ups = 30  # Updates per second
sups = 1  # Updates per second to server
reset_threshold = 1.4 * 60

# RootNode settings
interaction_end_threshold = 20  # End timer in seconds
location = "TUDelft Industrial Design faculty, Delft, The Netherlands"
ISO_location = "Delft,NL"

# Intensity settings
intensity_growth = 1
intensity_falloff_factor = 1
intensity_falloff_start = 10

# Touch sensor settings
touch_sensor_calibration_points = 10
touch_sensor_threshold = 4
touch_sensor_count_threshold = 5
touch_calibration_skips = 10

"""Environment settings"""
environment = Environment.Production
updates_per_second = 30
debug = False

"""Wifi settings"""
wifi = SimpleNamespace()
wifi.check_interval = 30
wifi.connection_attempts = 2
wifi.mqtt_broker = "rjrietdijk.com"
wifi.mqtt_broker_port = 1883
wifi.mqtt_broker_username = "ie_minor"
wifi.mqtt_broker_password = "wieditleesttrekteenbak"
wifi.secrets = {"ssid": ["OnePlus 9", ".", "Marie's iPhone", "capibara"], "password": ["g95zvuhm", "doobadoo", "birteboo123", "09060110"]}

mqtt_prepend = f"{project_name}/{system_id}"
