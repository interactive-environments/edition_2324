import time
import board
from digitalio import DigitalInOut, Direction, Pull

class DualButton :

    btn_1 = None
    btn_2 = None

    current_btn1_state = None
    current_btn2_state = None

    def __init__(self, PIN_1=board.A0, PIN_2=board.A1):

        self.btn_1 = DigitalInOut(PIN_1)
        self.btn_2 = DigitalInOut(PIN_2)

        self.current_btn1_state = self.btn_1.value
        self.current_btn2_state = self.btn_2.value

    def btn1_pressed(self):

        # The flag is used to detect whether the button has been pressed once,
        # without it the function would return True for the whole time the button is being pressed

        flag = self.current_btn1_state != self.btn_1.value  
        self.current_btn1_state = self.btn_1.value
        return flag and not self.btn_1.value 

    def btn2_pressed(self):

        # The flag is used to detect whether the button has been pressed once,
        # without it the function would return True for the whole time the button is being pressed

        flag = self.current_btn2_state != self.btn_2.value
        self.current_btn2_state = self.btn_2.value
        return flag and not self.btn_2.value

