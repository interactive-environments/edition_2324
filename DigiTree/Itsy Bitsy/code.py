from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from digitalio import DigitalInOut
import board
import busio
import time
import pwmio
from digitalio import DigitalInOut, Direction, Pull


solenoid_pins = [
    DigitalInOut(board.D13),
    DigitalInOut(board.D7),
    DigitalInOut(board.A0),  # Using A0 instead of D4
    DigitalInOut(board.A3),  # Using A3 instead of D3
    DigitalInOut(board.D2),
]

for pin in solenoid_pins:
    pin.direction = Direction.OUTPUT

OFFSET = 5

'''
=================== MQTT SETUP ===================
'''

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# If you have an externally connected ESP32:
esp32_cs = DigitalInOut(board.D9)  # Chip select pin
esp32_ready = DigitalInOut(board.D11)  # BUSY or READY pin
esp32_reset = DigitalInOut(board.D12)  # Reset pin


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# --- MQTT Functions
MQTT_topic = 'Activity'
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT broker! Listening for topic changes on %s" % MQTT_topic)
    # Subscribe to all changes on the default MQTT topic feed.
    client.subscribe(MQTT_topic)
    client.subscribe('Group-3/Data')


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    global last_incoming_value
    """Method callled when a client's subscribed feed has a new
   value.
   :param str topic: The topic of the feed with a new value.
   :param str message: The new value
   """
    if topic == MQTT_topic:
        last_incoming_value = float(message)
    elif topic == "Group-3/Data":
        print(f"Incoming Data: {message}")
        num = int(message) - OFFSET
        if 0 <= num < 5:
            print(f"Activating solenoid {num}")
            solenoid_pins[num].value = True
            time.sleep(0.5)
            solenoid_pins[num].value = False
            time.sleep(1)


# Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected!")


# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, esp)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    username=secrets["mqtt_broker_user"],
    password=secrets["mqtt_broker_password"],
    client_id=secrets["mqtt_client_id"]
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message


# Connect the client to the MQTT broker.
print("Connecting to MQTT broker...")
mqtt_client.connect()

# We will use this value to save new incoming data
last_incoming_value = 0


# Main loop
while True:
	# This try / except loop is used to continuously get new data from MQTT, and reset if anything goes wrong
    try:
        mqtt_client.loop(timeout=0.01)
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        mqtt_client.reconnect()
        continue

    mqtt_client.publish("Group-3/Activity", 64) # Send an activity update
    # print(last_incoming_value) # Activity level
    # Wait for some time before the next cycle
    time.sleep(0.1)  # Adjust the delay as needed


'''
======================================================
'''