import board
import random
import time

from LedStrip import Led_strip
from MQTT import MQTT_setup, on_message

'''
LEDS PER HEXAGON:
1: 21
2: 28
3: 34
4: 37

GROUPS HEXAGONS:
Red: 4,2,1
Orange: 3,4
Yellow: 2,1,4
Green: 4
Light blue: 4
Dark blue: 1,3,2
Purple: 1,3,4
Pink: 3,4

'''


RED = (255, 0, 0)
LIGHT_RED = (255, 40, 0)
ORANGE = (255, 70, 0)
LIGHT_ORANGE = (255, 100, 0)
YELLOW = (255, 120, 0)

GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 255, 127)

BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

REDDISH_PURPLE = (180, 0, 128)
PURPLE = (128, 0, 128)
PINK = (255, 20, 147)
MAGENTA = (255, 0, 255)

WHITE = (255, 255, 255)


red_group = Led_strip(
    pin=board.D13,
    num_pixels=86,
    group_colors=[PINK, MAGENTA, PURPLE],
    led_groups=[37, 28, 21]
)

orange_group = Led_strip(
    pin=board.D10,
    num_pixels=71,
    group_colors=[PURPLE, REDDISH_PURPLE],
    led_groups=[34, 37]
)

yellow_group = Led_strip(
    pin=board.D7,
    num_pixels=86,
    group_colors=[RED, LIGHT_RED, ORANGE],
    led_groups=[28, 21, 37]
)

green_group = Led_strip(
    pin=board.D4,
    num_pixels=37,
    group_colors=[ORANGE],
    led_groups=[37]
)

dark_blue_group = Led_strip(
    pin=board.D2,
    num_pixels=83,
    group_colors=[ORANGE, LIGHT_ORANGE, YELLOW],
    led_groups=[21, 34, 28]
)

light_blue_group = Led_strip(
    pin=board.D3,
    num_pixels=37,
    group_colors=[YELLOW],
    led_groups=[37]
)

purple_group = Led_strip(
    pin=board.A1,
    num_pixels=92,
    group_colors=[ORANGE, LIGHT_ORANGE, LIGHT_ORANGE],
    led_groups=[21, 34, 37]
)

pink_group = Led_strip(
    pin=board.A0,
    num_pixels=71,
    group_colors=[LIGHT_ORANGE, YELLOW],
    led_groups=[34, 37]
)

'''
    Paths: 
    - First: Red, Orange, Yellow
    - Second: Red, Orange, Yellow, Green, Dark Blue, Light Blue
    - Third: Red, Orange, Yellow, Green, Purple, Pink
'''

def shut_all_off():
    red_group.turn_off()
    orange_group.turn_off()
    yellow_group.turn_off()
    green_group.turn_off()
    dark_blue_group.turn_off()
    light_blue_group.turn_off()
    purple_group.turn_off()
    pink_group.turn_off()

def turn_all_on():
    red_group.stepstone()
    orange_group.stepstone()
    yellow_group.stepstone()
    green_group.stepstone()
    dark_blue_group.stepstone()
    light_blue_group.stepstone()
    purple_group.stepstone()
    pink_group.stepstone()

def trigger_chess_path():
    red_group.stepstone()
    orange_group.stepstone()
    yellow_group.stepstone()

def trigger_hammock_path():
    red_group.stepstone()
    orange_group.stepstone()
    yellow_group.stepstone()
    green_group.stepstone()
    dark_blue_group.stepstone()
    light_blue_group.stepstone()

def trigger_totem_path():
    red_group.stepstone()
    orange_group.stepstone()
    yellow_group.stepstone()
    green_group.stepstone()
    purple_group.stepstone()
    pink_group.stepstone()


shut_all_off()
MQTT = MQTT_setup()


# --- Main loop
while True:


    MQTT.loop()
    msg = MQTT.get_last_message()
    
    if msg == 'trigger':
        n = random.randint(1, 2)

        if n == 1:
            trigger_chess_path()
        elif n == 1:
            trigger_hammock_path()
        else:
            trigger_totem_path()

        MQTT.publish('biochair/turn_on_hexagons', 'off')
        shut_all_off() 


    time.sleep(.3)