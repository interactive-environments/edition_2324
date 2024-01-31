import time
import board
import busio
import json
import digitalio
import adafruit_rgbled
import config
import InputNode
import RootNode
import microcontroller

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import PWMOut
from wifi_client import WiFiClient
from utils.enums import Environment


def main():
    print(
        f"{config.device_id}: Runnning {config.project_name} v{config.version} in {config.environment} mode"
    )

    # Setup for the board LED
    BOARD_LED = digitalio.DigitalInOut(board.LED)
    BOARD_LED.direction = digitalio.Direction.OUTPUT
    BOARD_LED.value = True

    # Setup ESP pins for the wifi client
    esp32_cs = digitalio.DigitalInOut(board.CS1)
    esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
    esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
    esp = adafruit_esp32spi.ESP_SPIcontrol(
        spi, esp32_cs, esp32_ready, esp32_reset, debug=False
    )

    # Setup the WiFi status indicator LED
    RED_LED = PWMOut.PWMOut(esp, 27)
    GREEN_LED = PWMOut.PWMOut(esp, 26)
    BLUE_LED = PWMOut.PWMOut(esp, 25)
    status_light = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED, invert_pwm=True)

    # Setup the WiFi client
    wifi_client = WiFiClient(
        esp,
        config.wifi.secrets,
        status_pixel=status_light,
        attempts=config.wifi.connection_attempts,
        debug=config.debug,
    )

    MQTT.set_socket(socket, esp)
    mqtt_client = MQTT.MQTT(
        socket_timeout=0.01,
        broker=config.wifi.mqtt_broker,
        port=config.wifi.mqtt_broker_port,
        username=config.wifi.mqtt_broker_username,
        password=config.wifi.mqtt_broker_password,
        client_id=f"{config.mqtt_prepend}/arduino-{config.device_id}",
    )
    mqtt_client.on_connect = lambda client, userdata, flags, rc: print(
        "Connected to broker!"
    )
    mqtt_client.on_disconnect = lambda client, userdata, rc: print(
        "Disconnected from broker!"
    )
    mqtt_subsriptions = [
        (f"{config.mqtt_prepend}/state", 0),
        (f"{config.mqtt_prepend}/reset", 0),
    ]

    node = None
    if config.node_type == InputNode:
        node = InputNode.InputNode(mqtt_client)
        mqtt_subsriptions.append((f"{config.mqtt_prepend}/color_seed", 0))
    elif config.node_type == RootNode:
        node = RootNode.RootNode(mqtt_client)
        mqtt_subsriptions.append((f"{config.mqtt_prepend}/input_data", 0))
        mqtt_subsriptions.append((f"{config.mqtt_prepend}/image_sent", 0))
    else:
        raise ValueError(f"{config.node_type} is not a valid node type")
    mqtt_client.on_message = lambda client, topic, message: node.parse_message(
        client, topic, message
    )

    _previous_wifi_check = -config.wifi.check_interval
    running = True
    """ Main loop """
    while running:
        if config.environment == Environment.Production:
            """Production loop (WiFi enabled)"""
            try:
                # Check the connection of the wifi client and socketio client at the given interval
                if time.monotonic() - _previous_wifi_check > config.wifi.check_interval:
                    try:
                        if not wifi_client.is_connected():
                            wifi_client.connect()
                        if (
                            wifi_client.is_connected()
                            and not mqtt_client.is_connected()
                        ):
                            mqtt_client.connect()
                            if mqtt_client.is_connected():
                                mqtt_client.subscribe(mqtt_subsriptions)
                                if config.node_type == InputNode:
                                    mqtt_client.publish(
                                        f"{config.mqtt_prepend}/input_data",
                                        json.dumps(node.data),
                                    )
                                else:
                                    node.generate_seed()
                                    mqtt_client.publish(f"{config.mqtt_prepend}/reset", "true")
                                node.set_state("idle")
                    except Exception as e:
                        print("Error in establishing connection:", e)
                        node.set_state("disconnected")
                    finally:
                        _previous_wifi_check = time.monotonic()
                if mqtt_client.is_connected():
                    try:
                        mqtt_client.loop(timeout=0.01)
                    except (MQTT.MMQTTException, ConnectionError) as e:
                        if mqtt_client.is_connected():
                            try:
                                mqtt_client.disconnect()
                            except Exception as e:
                                print(e)
                node.loop()
            except Exception as e:
                print(e)
                if mqtt_client.is_connected():
                    mqtt_client.disconnect()
                running = False
                microcontroller.reset()

        elif config.environment == Environment.Development:
            """Development loop (WiFi disabled)"""
            try:
                node.loop()
            except Exception as e:
                print(e)
                running = False
                microcontroller.reset()
        time.sleep(1 / config.ups)

try:
    main()
except Exception as e:
    print(e)
    microcontroller.reset()
