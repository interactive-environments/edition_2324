import board
import time
import digitalio

class SharpIR:
    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT

    def read(self):
        self.pin.direction = digitalio.Direction.OUTPUT
        self.pin.value = False
        time.sleep(0.00002)
        self.pin.direction = digitalio.Direction.INPUT
        while not self.pin.value:
            pass
        start_time = time.time()
        while self.pin.value:
            pass
        end_time = time.time()
        duration = end_time - start_time
        distance = (duration * 34300) / 2
        return distance
