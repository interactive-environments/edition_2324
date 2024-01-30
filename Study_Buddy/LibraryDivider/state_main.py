import board
import time
from State import State
from TM1637 import TM1637 as DigitsDisplay 

from idle import idle
from card_scanned import card_scanned
from studying import studying
from break_f import break_f

from components.NeopixelLED import NeopixelLED
from components.Button import Button
from components.LCD import LCD
from components.RFID import RFID
from components.OLED_Display import OLED

STUDY_TIME_MINUTES = .1

class Main:

    start_btn = Button(pin=board.A0)    # Button to transition between specific states 
    reset_btn = Button(pin=board.A2)    # Button to reset routine to Idle

    study_led = NeopixelLED(num_leds=1, port_leds=board.D13, brightness=.1)  
    break_led = NeopixelLED(num_leds=1, port_leds=board.D7, brightness=.5) 

    lcd = LCD()             #LCD display - I2C port
    rfid = RFID()           #RFID card scanner - UART port
    oled_display = OLED()   #Square OLED display - I2C port

    points_display = DigitsDisplay(board.D2, board.D3)  # 7 segments 4 digit display

    # Components dictionary passed to each state function
    components = {
        'start_button': start_btn,
        'reset_button': reset_btn,
        'study_led': study_led,
        'break_led': break_led,
        'lcd': lcd,
        'rfid': rfid,
        'points_display': points_display,
        'oled': oled_display
    }

    state = State()     # Object to control states
    start_time = None   # Checks when study time starts

    oled_display.show('./assets/qr.bmp')

    state.print_state() # Prints current state in the console before the start of the routine 

    def __init__(self): 

        # Start of routine
        while True:

            if self.reset_btn.pressed():
                self.reset()


            #* Idle state - Wait for campus card to be scanned
            if self.state.is_idle():
                idle(self.state, self.components)


            #* Card scanned - Wait for user to press button
            elif self.state.is_card_scanned():
                card_scanned(self.state, self.components)


            #* Studying - Wait for study time to expire
            elif self.state.is_studying():
                studying(STUDY_TIME_MINUTES, self.state, self.components)
                

            #* Break - Wait for user to scan campus card again
            elif self.state.is_break():
                break_f(self.state, self.components)


            #* Reset parameters for next iteration
            else:
                self.reset()


            time.sleep(.2)

    def reset(self):
        self.start_time = None
        self.state.setup_flag = True
        self.lcd.clear()
        self.state.set_idle()
        self.state.print_state()  



Main()