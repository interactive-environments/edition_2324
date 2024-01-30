import os
import board
import busio
import time
import digitalio
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import neopixel
import adafruit_minimqtt.adafruit_minimqtt as MQTT

from secrets import secrets

# Add settings.toml to your filesystem CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD keys
# with your WiFi credentials. Add your Adafruit IO username and key as well.
# DO NOT share that file or commit it into Git or other source control.

mqtt_topic = secrets['mqtt_topic']
mqtt_broker = secrets['mqtt_broker']


# Define the pins used by the BitsyExpander's ESP32 WiFi module
esp32_cs = digitalio.DigitalInOut(board.D9)
esp32_ready = digitalio.DigitalInOut(board.D11)
esp32_reset = digitalio.DigitalInOut(board.D12)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
   

# Initialize the ESP32 WiFi module
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

onboard_led = neopixel.NeoPixel(board.NEOPIXEL, 1)
onboard_led.brightness = 0.1

onboard_led[0] = (255, 0, 0)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue

print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi, "\tIP: ", esp.pretty_ip(esp.ip_address))

onboard_led[0] = (0, 255, 0)

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code %d" % (rc))
    client.subscribe(mqtt_topic)

def on_message(client, topic, message):
    print("Received message on topic {}: {}".format(topic, message))

socket.set_interface(esp)
MQTT.set_socket(socket)

# Set up a MiniMQTT Client
client = MQTT.MQTT(
    broker=mqtt_broker,
    username='itsybitsy',  # if you have authentication
    password=None   # if you have authentication
)

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect()

# Start the loop to listen for messages
client.loop_forever()