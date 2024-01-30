import board 
from digitalio import DigitalInOut, Direction, Pull

class Button :

    button = None
    button_state = None

    def __init__(self, pin=board.A0):

        self.button = DigitalInOut(pin)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP
        self.button_state = self.button.value

    def pressed(self):

        # The flag is used to detect whether the button has been pressed once,
        # without it the function would return True for the whole time the button is being pressed

        flag = self.button_state != self.button.value  
        self.button_state = self.button.value
        return flag and not self.button.value 
