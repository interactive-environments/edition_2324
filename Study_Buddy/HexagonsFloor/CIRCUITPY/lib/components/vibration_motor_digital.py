# vibration motor

import board
import digitalio

class VibrationMotor():
    def __init__(self,port=board.D2):
        self.motor = digitalio.DigitalInOut(port)
        self.motor.direction = digitalio.Direction.OUTPUT

    # Takes either true or false
    def update(self, value):
        self.motor.value = value
