import time

def idle(components, state, MQTT_client):

    sit_flag = MQTT_client.get_last_message()
    #sit_flag = True

    if sit_flag:
        state.switch_state()


def person_sat(components, state, MQTT_client):

    led_strip_divider = components['led_strip_divider']
    scanner_led = components['scanner_led']
    rfid = components['rfid']

    sit_flag = MQTT_client.get_last_message()
    #sit_flag = True

    if state.setup_flag:
        scanner_led.color((100, 0, 0, 0))
        state.set_flag_false()

    if not sit_flag:
        print('User stood up, going back to idle')
        led_strip_divider.turn_off()
        state.reset_state()

    if rfid.get_data() is not None:
        state.switch_state()


def card_scanned(components, state):

    led_strip_divider = components['led_strip_divider']
    scanner_led = components['scanner_led']

    if state.setup_flag:
        scanner_led.turn_off()
        led_strip_divider.fillup(.1)
        led_strip_divider.visual_timer(20)
        state.set_flag_false()

    state.switch_state()


def timer_ended(components, state, MQTT_client):

    sit_flag = MQTT_client.get_last_message()
    led_strip_divider = components['led_strip_divider']

    if state.setup_flag:
        led_strip_divider.flash()
        state.set_flag_false()

    print(sit_flag)
    if not sit_flag:
        state.switch_state()


def user_stands_up(components, state, MQTT_client):

    MQTT_client.publish('biochair/turn_on_hexagons', 'trigger')
    print('Trigger sent to hexagons')

    time.sleep(5)
    state.switch_state()
