def idle (state, components):

    study_led = components['study_led']
    break_led = components['break_led']
    rfid = components['rfid']
    points_display = components['points_display']
    lcd = components['lcd']
    oled = components['oled']

    if state.setup_flag:

        points_display.number(0)
        lcd.print('Scan your campuscard...') 

        state.set_flag_false()

    study_led.update_full_color((0, 255, 0, 0))
    break_led.update_full_color((0, 0, 0, 0))

    if rfid.get_data() is not None:
        state.switch_state()
