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

mqtt_password = secrets['mqtt_broker_password']
mqtt_username = secrets['mqtt_broker_user']
mqtt_client_id = secrets['mqtt_client_id']

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
last_message = None

mac_addr = ":".join("{:02X}".format(byte) for byte in reversed(esp.MAC_address))
print(mac_addr)

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code %d" % (rc))
    client.subscribe(mqtt_topic)

def on_message(client, topic, message):

    #print(message)
    """     data, sit_flag = message.split(',')

    parsed_data = None

    try:
        parsed_data = int(data)
    except:
        pass

    parsed_flag = False if sit_flag == 'False' else True if sit_flag == 'True' else None
    """
    if message:
        set_last_message(message) 

def set_last_message(msg):
    global last_message
    last_message = msg

def get_last_message():
    global last_message
    return last_message

def MQTT_setup():

    print("\nConnecting to AP...")
    while not esp.is_connected:
        try:
            esp.connect_AP(secrets["ssid"], secrets["password"])
        except RuntimeError as e:
            print("could not connect to AP, retrying: ", e)
            continue

    onboard_led[0] = (0, 255, 0)

    print("\nConnected to", str(esp.ssid, "utf-8"), "\tIP: ", esp.pretty_ip(esp.ip_address))

    socket.set_interface(esp)
    MQTT.set_socket(socket)

    # Set up a MiniMQTT Client
    client = MQTT.MQTT(
        client_id=mqtt_client_id,
        broker=mqtt_broker,
        username=mqtt_username,  # if you have authentication
        password=mqtt_password   # if you have authentication
    )

    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.get_last_message = get_last_message

    # Connect to MQTT broker
    client.connect()

    return client