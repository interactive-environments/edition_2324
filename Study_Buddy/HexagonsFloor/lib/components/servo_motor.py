# servo_motor.py

import board
import pwmio
from adafruit_motor import servo

class Servo():
    def __init__(self, port=board.D4):
        self.pwm = pwmio.PWMOut(port, frequency = 50)
        self.servo = servo.Servo(self.pwm)
        self.lastAngle = 0

    # Takes a value between 0 and 180
    def update(self, angle):
        if angle == self.lastAngle:
            return

        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        self.servo.angle = angle
        self.lastAngle = angle
