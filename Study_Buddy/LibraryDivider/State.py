# State controller class
class State:

    # Available states
    IDLE = 1            # Lights randomly light up to attract attention
    PERSON_SAT = 2      # Fill up lights
    CARD_SCANNED = 3    # Start timer and turn off LEDs one by one
    TIMER_ENDED = 4     # Flash lights and wait for user to stand up
    USER_STANDS_UP = 5  # Light up lights on the floor

    state_str_array = [
        'Idle',
        'User sat down',
        'Card scanned',
        'Timer ended',
        'User stood up'
    ]

    state_array = [
        IDLE,
        PERSON_SAT,
        CARD_SCANNED,
        TIMER_ENDED,
        USER_STANDS_UP
    ]

    state_index = None

    current_state = None # Keeps track of current state

    setup_flag = True

    def __init__(self):
        self.state_index = 0
        self.current_state = self.state_array[self.state_index]
        self.print_state()

    # Switches to next stte based on current state
    def switch_state(self):

        self.setup_flag = True

        if self.state_index == len(self.state_array) - 1:
            self.state_index = 0

        else:
            self.state_index += 1

        self.current_state = self.state_array[self.state_index]
        self.print_state()

    def reset_state(self):
        self.state_index = 0
        self.current_state = self.state_array[self.state_index]

    def set_flag_false(self):
        self.setup_flag = False

    def print_state(self):
        print(f'*** Current state: {self.state_str_array[self.state_index]} ***')
