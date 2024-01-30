from components.button import Button
from components.buzzer import Buzzer
from components.led import LED
from components.servo_motor import Servo
from components.slider import Slider
import board
import random

button = Button()
buzzer = Buzzer()
led = LED(1)
servo = Servo()
slider = Slider(port=board.A4)

increase = True
led_power = 255
color = (1, 0, 0)
direction = "increase"
servo_step = 0
prev_button_value = False

# CREATURE: Movement
# This creature will simulate 3 states:
# 1) neutral: shows white light and relaxed servo movement
# 2) happy: shows green light and no servo movement
# 3) angry: shows red light and fast servo movement
# If the button is pressed the creature will compleetly freeze

class Creature:

    def __init__(self):
        self.ecosystem = None

    def message(self, msg):
        global color, servo_step
        print("recieved: " + str(msg))
        if msg == "ping": #simulate a neutral statee with white light and slow servo
            color = (1,0,0)
            servo_step = 5

        # Send the ping message when we recive pong
        if msg == "pong": #simulate a happy state with green light and no servo
            color = (0, 1, 0)
            servo_step = 0
            # There is a 25% change that we will repley with ping
            if random.randint(0,3) == 3:
                self.ecosystem.send_message("ping")

        if msg == "pow": #simulate an angry state with white light and fast servo
            color = (200, 200, 200)
            servo_step = 1

    def sense(self):
        if button.sense() == True:
            return True

    # One iteration of the creatures main loop
    def loop(self):
        global increase, led_power, color, direction, servo_step, prev_button_value

        # If the button is pressed it will freeze
        if self.sense():
            return

        # increase or decease the brightness by 1 every loop.
        if increase:
            led_power += 1
            if led_power > 255:
                led_power = 255
                increase = False
        else:
            led_power -= 1
            if led_power < 0:
                led_power = 0
                increase = True
                
        # Determine whether we need to decrease or increase the servo angle        
        if direction == "increase":
            new_angle = servo.lastAngle + servo_step
        elif direction == "decrease":
            new_angle = servo.lastAngle - servo_step
            
        # update the servo angle
        if (new_angle < 0):
            new_angle = 0
            direction = "increase"
        elif (new_angle > 180):
            new_angle = 180
            direction = "decrease"
        servo.update(new_angle)
        servo.lastAngle = new_angle


        # show the led color
        actual_color = tuple([led_power * c for c in color])
        led.update_full_color(actual_color)
