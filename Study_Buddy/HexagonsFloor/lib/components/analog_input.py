import board
import analogio

class AnalogInput():
    def __init__(self, port=board.A0):
        self.input = analogio.AnalogIn(port)

    def sense(self, threshold):
        return self.input.value > threshold

    def sense_value(self):
        return self.input.value / 65536 * 100
