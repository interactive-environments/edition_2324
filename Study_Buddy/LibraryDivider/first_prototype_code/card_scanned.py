def card_scanned(state, components):

    start_button = components['start_button']
    points_display = components['points_display']
    lcd = components['lcd']

    if state.setup_flag:

        points_display.number(15)
        lcd.clear()
        lcd.print('Press start to  start studying') # No space because it goes to the next line
        state.set_flag_false()
    
    if start_button.pressed():
       state.switch_state()