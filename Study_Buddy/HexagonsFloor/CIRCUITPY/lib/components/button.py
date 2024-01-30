# button.py

import board
import digitalio

class Button():
    previous_button_value = False

    def __init__(self, port=board.A2):
        self.button = digitalio.DigitalInOut(port)
        self.button.direction = digitalio.Direction.INPUT

    def sense(self):
        button_status = False
        current_button_value = self.button.value

        # Only trigger on button down
        if (current_button_value == True):
            button_status = True

        return button_status

    def sense_release(self):
        current_button_value = self.button.value
        button_status = False

        # Only trigger on button release
        if (self.previous_button_value == True and current_button_value == False):
            button_status = True

        self.previous_button_value = current_button_value

        return button_status
