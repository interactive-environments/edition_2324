# buzzer.py 

import board
import time
import pwmio

class Buzzer():

    volume = 30
    playing = False

    def __init__(self, port=board.D7):
        self.buzzer = pwmio.PWMOut(port, frequency = 50, variable_frequency=True)

    # Takes a value between 0 and 100, then scales it up.
    def update(self, volume):
        scaledVolume = volume/100*16383
        self.buzzer.duty_cycle = int(scaledVolume)

    def set_frequency(self, fq):
        self.buzzer.frequency = 1 if fq == 0 else fq

    def play_chime(self, forward):

        if not self.playing:

            self.playing = True
            self.update(self.volume)
            frequencies = [1500, 2000, 2500]

            list = frequencies if forward else reversed(frequencies)

            for fq in list:
                self.set_frequency(fq)
                time.sleep(.25)

            self.update(0)

            self.playing = False

    def play_finish_time(self):

        if not self.playing:

            self.playing = True
            self.update(self.volume)
            frequencies = [1500, 1000, 1500, 2000, 2500, 3000]

            for fq in frequencies:
                self.set_frequency(fq)
                time.sleep(.225)

            self.update(0)

            self.playing = False