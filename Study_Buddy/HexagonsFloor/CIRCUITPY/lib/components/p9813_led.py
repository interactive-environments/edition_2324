
import board
import p9813

class P9813LED():
    def __init__(self, num_leds=2,port_clk=board.D13,port_data=board.D10):
        self.pin_clk = port_clk
        self.pin_data = port_data
        self.num_leds = num_leds
        self.leds = p9813.P9813(self.pin_clk, self.pin_data, self.num_leds)

    # Update the LED with specified intensity for all three color channels
    def update(self, color):
#         intensity = max(color[0], max(color[1], color[2]))
#         color = max(0, min(intensity, 255))
        self.leds[0] = (color[0], color[1], color[2])
        self.leds[1] = (255-color[0], 255-color[1], 0)
        self.leds.write()

    # Update the LED with a tuple of (RED, GREEN, BLUE)
    def update_full_color(self, color):
        clipped_color = (max(0, min(color[0], 255)),
            max(0, min(color[1], 255)),
            max(0, min(color[2], 255)))
        self.leds.fill(clipped_color)
        self.leds.write()
