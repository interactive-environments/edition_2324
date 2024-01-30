import math
import time

def studying(study_time, state, components):

    study_led = components['study_led']
    lcd = components['lcd']

    if state.setup_flag:
        #print(f"\nTimer set for {STUDY_TIME_MINUTES} minutes.\n")
        start_time = time.time()

        lcd.clear()
        lcd.print('Study time')
        lcd.lcd_print_progress_bar(study_time)
        study_led.update_full_color((0, 255, 0, 0))

        state.set_flag_false()

    elapsed_seconds = time.time() - start_time

    remaining_minutes = study_time - (elapsed_seconds / 60)

    # Study time finished
    if remaining_minutes <= 0:
        study_led.update_full_color((0, 0, 0, 0))
        state.switch_state()

    #print_remaining_time(elapsed_seconds, remaining_minutes)



def print_remaining_time(elapsed_seconds, remaining_minutes):

    current_seconds = "{0:0=2d}".format(59 - (elapsed_seconds % 60))
    floored_minutes = "{0:0=2d}".format(math.ceil(remaining_minutes) - 1)
    print(f"Time remaining: \t{floored_minutes}:{current_seconds}\t", end='\r')  # Print countdown on the same line