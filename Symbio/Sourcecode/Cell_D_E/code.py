from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from digitalio import DigitalInOut
from slider import Slider
import board
import busio
import time
import pwmio
import digitalio


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


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    global last_incoming_value
    """Method called when a client's subscribed feed has a new
   value.
   :param str topic: The topic of the feed with a new value.
   :param str message: The new value
   """
    print("New message on topic {0}: {1}".format(topic, message))
    last_incoming_value = float(message)


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
    client_id=secrets["mqtt_clientid"]
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


###########################################

# Create PWMOut objects for fan control
hub_D_fan_in = pwmio.PWMOut(board.D7, frequency=5000, duty_cycle=0)
hub_D_fan_out = pwmio.PWMOut(board.D4, frequency=5000, duty_cycle=0)
hub_D_fan_mist = pwmio.PWMOut(board.D13, frequency=5000, duty_cycle=0)

hub_E_fan_in = pwmio.PWMOut(board.D3, frequency=5000, duty_cycle=0)
hub_E_fan_out = pwmio.PWMOut(board.D2, frequency=5000, duty_cycle=0)
hub_E_fan_mist = pwmio.PWMOut(board.A0, frequency=5000, duty_cycle=0)
curState = 0

slider = Slider()

def adjust_fans(value_fan_in, value_fan_out, value_fan_mist, hub_fan_in, hub_fan_out, hub_fan_mist):
    hub_fan_in.duty_cycle = int(65535 * value_fan_in)
    hub_fan_out.duty_cycle = int(65535 * value_fan_out)
    hub_fan_mist.duty_cycle = int(65535 * value_fan_mist)

def crowded():
    global curState, now
    if time.monotonic() - now > 12:
        curState = 0
        mqtt_client.publish("Group-1/Activity", 1) # Send an activity update
    elif time.monotonic() - now > 11:
        adjust_fans(0, 0, 1, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0.7, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 7:
        adjust_fans(0, 0.33, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0.30, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 4.5:
        adjust_fans(1, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    else:
        adjust_fans(1, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(1, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)

def busy():
    global curState, now
    if time.monotonic() - now > 15:
        curState = 0
        mqtt_client.publish("Group-1/Activity", 1) # Send an activity update
    elif time.monotonic() - now > 14:
        adjust_fans(0, 0, 1, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0.7, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 8:
        adjust_fans(0, 0.25, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0.17, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 4.5:
        adjust_fans(0, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    else:
        adjust_fans(0.75, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0.25, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)


def quiet():
    global curState, now
    if time.monotonic() - now > 22:
        curState = 0
        mqtt_client.publish("Group-1/Activity", 1) # Send an activity update
        hubD_timer = time.monotonic()
    elif time.monotonic() - now > 19:
        adjust_fans(0, 0, 1, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0.7, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 11:
        adjust_fans(0, 0.15, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0.10, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    elif time.monotonic() - now > 4.5:
        adjust_fans(0, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)
    else:
        adjust_fans(0.3, 0, 0, hub_D_fan_in, hub_D_fan_out, hub_D_fan_mist)
        adjust_fans(0.22, 0, 0, hub_E_fan_in, hub_E_fan_out, hub_E_fan_mist)


def get_selected_message():
    global curState, now
    if curState == 0:
        maxValue = 1 #max value of the environment: want to divide slider in 3 intervals to determine which message is being sent
        #print(last_incoming_value) # Activity level
        if slider.sense() < 300:
            curValue = last_incoming_value
        else:
            curValue = (slider.sense() + 8000)/100000
        curValue = 0.20
        if(curValue > 0.67):
            curState = 1
            now = time.monotonic()
        elif(curValue > 0.34):
            curState = 2
            now = time.monotonic()
        else:
            curState = 3
            now = time.monotonic()
    elif curState == 1:
        crowded()
    elif curState == 2:
        busy()
    elif curState == 3:
        quiet()
    print(curState)

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

    get_selected_message()
    #print(last_incoming_value) # Activity level
    # Wait for some time before the next cycle
    time.sleep(1)  # Adjust the delay as needed
