from components.button import Button
from components.led import LED
from timer import Timer
from components.vibration_motor_digital import VibrationMotor
import random

button = Button()
led = LED(1)
vibration_motor = VibrationMotor()

count = 255
color = (1, 0, 0)

prev_message = ""
send_timer = Timer()
send_timer.set_duration(1)

count = 0
count_to = 2

# CREATURE: Observer
# This creature will keep count of the messages.
# Every time a new messages is send that is different from the previous the count will reset.
# the pong count is blue.
# the ping count is green.
# the pow count is red.
# it will vibrate when the count reaches 255.
class Creature:

    def __init__(self):
        self.ecosystem = None

    def message(self, msg):
        global color, prev_message, count
        print("recieved: " + str(msg))
        
        # rest the count
        if msg != prev_message:
            count = 0
            prev_message = msg

        # We recieved ping
        if msg == "ping":
            # Set the color to blue
            color = (0,0,1)
            count += 1



        # Send the ping message when we recive pong
        if msg == "pong":
            # Set the color to green
            color  = (0,1,0)
            count += 1
            
            

        if msg == "pow":
            # Set the color to red
            color = (1, 0, 0)
            count += 1
            
            

    def sense(self):
        # Check if someone is within 200mm
        if button.sense_release() == True:
            return True

    # One iteration of the creatures main loop
    def loop(self):
        global color, count, count_to

        # message options
        options = ["ping", "pong", "pow"]

        # cap the count
        if count > count_to:
            count = count_to

        # Send random if we matched the count
        if count == count_to:
            #self.ecosystem.send_message(random.choice(options))
            # Start vibrating
            vibration_motor.update(True)
        else:
            # start vibrating
            vibration_motor.update(0)

        # If we sense someone is there
        if self.sense():
            count = 0


        
        actual_color = tuple([int((count * (255/count_to)  ) * c) for c in color])
        led.update_full_color(actual_color)
