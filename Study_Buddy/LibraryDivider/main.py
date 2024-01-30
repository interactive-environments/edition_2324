import time
import asyncio
import board

from State import State
from MQTT import MQTT_setup
from state_functions import idle, person_sat, card_scanned, timer_ended, user_stands_up

from components.Led_strip import Led_strip
from components.RFID import RFID
from components.Led import Led


# Start the loop to listen for messages
class Main:

    MQTT_client = None
    state =  None

    rfid = RFID()

    led_strip_divider = Led_strip(pin=board.D13, num_pixels=31, brightness=1.0)
    scanner_led = Led(pin=board.D3, num_pixels=64, brightness=1.0)


    led_strip_divider.turn_off()
    scanner_led.turn_off()

    # Components dictionary passed to each state function
    components = {
        'led_strip_divider': led_strip_divider,
        'scanner_led': scanner_led,
        'rfid': rfid,
    }

    #scanner_led.color((100, 0, 0, 0))

    def __init__(self):

        self.MQTT_client = MQTT_setup()

        self.state = State()

        while True:

            self.MQTT_client.loop()

            #* TODO: Replace with state description
            if self.state.current_state == self.state.IDLE:
                idle(self.components, self.state, self.MQTT_client)

            #* TODO: Replace with state description
            elif self.state.current_state == self.state.PERSON_SAT:
                person_sat(self.components, self.state, self.MQTT_client)

            #* TODO: Replace with state description
            elif self.state.current_state == self.state.CARD_SCANNED:
                card_scanned(self.components, self.state)

            #* TODO: Replace with state description
            elif self.state.current_state == self.state.TIMER_ENDED:
                timer_ended(self.components, self.state, self.MQTT_client)

            #* TODO: Replace with state description
            elif self.state.current_state == self.state.USER_STANDS_UP:
                user_stands_up(self.components, self.state, self.MQTT_client)

            time.sleep(.1)

    def reset(self):
        self.state.reset_state()

Main()
