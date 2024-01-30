def break_f(state, components):

    start_button = components['start_button']
    break_led = components['break_led']

    if state.setup_flag:
        state.set_flag_false()

    break_led.update_full_color((0, 0, 255, 0))

    if start_button.pressed():
       state.switch_state()