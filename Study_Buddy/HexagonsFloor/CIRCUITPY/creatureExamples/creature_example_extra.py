from components.button import Button
from components.led import LED
from components.slider import Slider
import board
import random
import time

button = Button()
led = LED(1)
slider = Slider(port = board.A4)

color = (1, 0, 0)
led_is_on = False
timer_mark = 0
timer_duration = 0

# This creature will have a flickering light.
# The incoming messages have a color channel and a colorvalue. 
# We adjust our led by changing the colorvalue of the appropriate colorchannel.
# The rgb value being sent is determined by the position of the slider. The color channel we put in the message is randomly assigned.
class Creature:

    def __init__(self):
        self.ecosystem = None

    #we check which RGB value we need to adjust, and set the correct rgb value to it
    def message(self, msg):
        global color
        print("recieved: " + str(msg))
        msg_list = msg.split("&&&") #split the string by a delimiter "&&&", and makes an array of the elements
        color_type = msg_list[0]
        rgb_value = int(msg_list[1])
        # Check for color, set it the correct value
        if color_type == "Red":
            color = (rgb_value, 20, 20)
        elif color_type == "Blue":
            color = (20, rgb_value, 20)
        elif color_type == "Green":
            color = (20, 20, rgb_value)



    def sense(self):
        if button.sense() == True:
            return True

    # This method prepared the message to be sent and returns is
    # We randomly choose which color channel we want to put int the message.
    # The slider determines how big the corresponding value will ne
    def get_selected_message(self):
        maxSLider = 65520; #max value of the slider: want to divide slider in 3 intervals to determine which message is being sent
        color_value = (slider.sense() / 65520) * 255
        rgb_list = ["Red", "Blue", "Green"]
        rgb_type = random.choice(rgb_list)
        return rgb_type + "&&&" + str(int(color_value))

    # A timer to check how much time has passed; used for flickering of the light
    def set_timer(self, duration):
        global timer_duration, timer_mark
        timer_duration = duration
        timer_mark = time.monotonic()

    # Use this to check if the timer has expired
    def timer_expired(self):
        global timer_mark, timer_duration
        if time.monotonic() - timer_mark > timer_duration:
            return True
        else:
            return False

    # One iteration of the creatures main loop
    def loop(self):
        global color, led_is_on

        # turn led on and off when timer expired
        if self.timer_expired():
            if led_is_on:
                led.update_full_color(color)
            else:
                led.update((0,0,0))
            led_is_on = not led_is_on
            self.set_timer(1)




