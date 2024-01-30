from components.tof import Tof
from components.led import LED
from timer import Timer
import random

tof = Tof()
led = LED(1)

increase = True
pulse = True
led_power = 255
color = (1, 0, 0)

next_message = ""
send_timer = Timer()
send_timer.set_duration(1)

# CREATURE: Defensive
# This creature will overtime randomly send messages.
# once someone gets to close it will keep sending the "pow" message
# on a ping message it will 75% of the times respond with pong and have blue slow pulsing light.
# on a ping message it will 75% of the time respond with ping and have green slow pulsing light.
# on a pow message it will not responed and have a constant red light
class Creature:

    def __init__(self):
        self.ecosystem = None

    def message(self, msg):
        global color, pulse, next_message
        print("recieved: " + str(msg))
        
        # We recieved ping
        if msg == "ping":
            # Set the color to blue
            color = (0,0,1)
            # Allow pulse
            pulse = True
            # Mage a almost acurate replie
            reply = random.randint(1,4)
            if reply > 3:
                next_message = "ping"
            else:
                next_message = "pong"


        # Send the ping message when we recive pong
        if msg == "pong":
            # Set the color to green
            color  = (0,1,0)
            # Allow pulse
            pulse = True
            # Mage a almost acurate replie
            chance = random.randint(1,4)
            if chance > 3:
                next_message = "pong"
            else:
                next_message = "ping"
            

        if msg == "pow":
            # Set the color to red
            color = (1, 0, 0)
            # Disable pulse
            pulse = False
            

    def sense(self):
        # Check if someone is within 200mm
        if tof.sense(200) == True:
            return True

    # One iteration of the creatures main loop
    def loop(self):
        global increase, led_power, color, pulse, send_timer, next_message

        panic = False

        # If we sense someone is there
        if self.sense():
            # Go into panic mode
            pulse = False
            color = (1,0,0)
            self.ecosystem.send_message("pow")
            panic = True

        # check if it is time to send somthing
        if send_timer.expired() and not panic:
            # next message will be within 1 and 5 seconds
            send_timer.set_duration(random.randint(1,5))
            send_timer.start()
            # send a message if we had one
            if next_message != "":
                self.ecosystem.send_message(next_message)
                # clear the message
                next_message = ""



        # increase or decease the brightness by 10 every loop.
        if increase:
            led_power += 10
            if led_power > 255:
                led_power = 255
                increase = False
        else:
            led_power -= 10
            if led_power < 0:
                led_power = 0
                increase = True

        # show the led color
        if pulse:
            # multiplies all the values in the color list by led power to set brightness 
            actual_color = tuple([led_power * c for c in color])
        else:
            # multiplies all the values in the color list by 255 for max brightness
            actual_color = tuple([255 * c for c in color])
        led.update_full_color(actual_color)
