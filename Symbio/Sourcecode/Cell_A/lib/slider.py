# slider.py
import time
import board
from analogio import AnalogIn
from analogio import AnalogOut
import pwmio

class Slider():
    def __init__(self, port=board.A2):
            self.slider = AnalogIn(port)

    def sense(self):
        return self.slider.value
