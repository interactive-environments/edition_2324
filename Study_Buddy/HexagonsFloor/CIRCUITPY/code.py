import board
import time

from LedStrip import Led_strip

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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (100, 0, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)


red_group = Led_strip(
    pin=board.D13,
    num_pixels=86,
    group_colors=[RED, MAGENTA, PURPLE],
    led_groups=[37, 28, 21]
)

orange_group = Led_strip(
    pin=board.D10,
    num_pixels=71,
    group_colors=[CYAN, BLUE],
    led_groups=[34, 37]
)

yellow_group = Led_strip(
    pin=board.D7,
    num_pixels=86,
    group_colors=[YELLOW, ORANGE, RED],
    led_groups=[28, 21, 37]
)

green_group = Led_strip(
    pin=board.D4,
    num_pixels=37,
    group_colors=[GREEN],
    led_groups=[37]
)

light_blue_group = Led_strip(
    pin=board.D3,
    num_pixels=37,
    group_colors=[BLUE],
    led_groups=[37]
)

dark_blue_group = Led_strip(
    pin=board.D2,
    num_pixels=83,
    group_colors=[PURPLE, BLUE, CYAN],
    led_groups=[21, 34, 28]
)

purple_group = Led_strip(
    pin=board.A1,
    num_pixels=92,
    group_colors=[ORANGE, GREEN, BLUE],
    led_groups=[21, 34, 37]
)

pink_group = Led_strip(
    pin=board.A0,
    num_pixels=71,
    group_colors=[PINK, MAGENTA],
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
    light_blue_group.turn_off()
    dark_blue_group.turn_off()
    purple_group.turn_off()
    pink_group.turn_off()

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

# --- Main loop
while True:

    shut_all_off()
    trigger_totem_path()


    time.sleep(3)
