import time

class Timer():
    def __init__(self, duration = 0):
        self.duration = duration
        self.time_mark = 0

    def start(self):
        self.time_mark = time.monotonic()

    def set_duration(self, duration):
        self.duration = duration

    def expired(self):
        if time.monotonic() - self.time_mark > self.duration:
            return True
        else:
            return False
