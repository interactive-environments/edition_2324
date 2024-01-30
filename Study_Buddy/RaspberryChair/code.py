import serial
import time
from serial_controller import get_serial_data 
import paho.mqtt.client as mqtt



# -- Serial configuration --
serial_port = '/dev/ttyACM0'
baud_rate = 9600

# -- MQTT configuration --
broker_address='ide-education.cloud.shiftr.io'
mqtt_username='ide-education'
mqtt_password='Sy0L85iwSSgc1P7E'
mqtt_client_id='RasPi-Biochair'

port=1883
topic='biochair/data'

# -- MQTT setup -- 

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    client.subscribe(topic)

def on_message(client, userdata, msg):
    filler = None
    #print(f'{msg.topic} {str(msg.payload)}')

client = mqtt.Client(client_id=mqtt_client_id)
client.username_pw_set(mqtt_username, password=mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_start()


# -- Code --

THRESHOLD = 7000
DATA_TRANSMISSION_INTERVAL = 1

while True:

    last_data, is_sudden_change = get_serial_data(THRESHOLD)
    if last_data:
        client.publish(topic, f'{last_data},{is_sudden_change}')

    time.sleep(DATA_TRANSMISSION_INTERVAL)
