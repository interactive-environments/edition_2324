import time
import board
import neopixel
import busio

num_pixels = 80
pixels = neopixel.NeoPixel(board.D10, num_pixels, brightness=0.2, auto_write=True, pixel_order=neopixel.GRB)

STUDY_TIME = 0.3

color_array = []

green = (0, 255, 0)
orange = (255, 165, 0)
red = (255, 0, 0)

for i in range(num_pixels):
    ratio = i / num_pixels
    if ratio <= 0.5:
        color = (
            int((1 - ratio * 2) * green[0] + ratio * 2 * orange[0]),
            int((1 - ratio * 2) * green[1] + ratio * 2 * orange[1]),
            int((1 - ratio * 2) * green[2] + ratio * 2 * orange[2])
        )
    else:
        ratio = (ratio - 0.5) * 2
        color = (
            int((1 - ratio) * orange[0] + ratio * red[0]),
            int((1 - ratio) * orange[1] + ratio * red[1]),
            int((1 - ratio) * orange[2] + ratio * red[2])
        )
    color_array.append(color)

def visual_timer():
    pixels.fill((0, 0, 0, 0))

    # Gradual color transition
    for i in range(num_pixels):
        pixels[i] = color_array[i]
        time.sleep(STUDY_TIME)

# Turn off LEDs initially
pixels.fill((0, 0, 0, 0))

# RFID setup
rfid = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.05)
last_card_id = None

while True:
    data = rfid.read(14)
    if data is not None:
        card_id = data.decode('utf-8')

        if card_id != last_card_id:
            print("Card read:", card_id)

            # Start the visual timer when a new card is scanned
            visual_timer()

            last_card_id = card_id
