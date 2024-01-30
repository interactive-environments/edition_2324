# buzzer.py 

import board
import pwmio

class Buzzer():
    def __init__(self, port=board.D7):
        self.buzzer = pwmio.PWMOut(port, frequency = 50)

    # Takes a value between 0 and 100, then scales it up.
    def update(self, volume):
        scaledVolume = volume/100*16383
        self.buzzer.duty_cycle = int(scaledVolume)

    def set_frequency(self, fq):
        self.buzzer.frequency = fq
