import board
import time
import displayio
import adafruit_display_text.bitmap_label as label # from adafruit_display_text
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297


class OLED:

    displayio.release_displays()

    # Use for I2C
    i2c = board.I2C()
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

    # SH1107 is vertically oriented 128x128
    WIDTH = 128
    HEIGHT = 128
    BORDER = 0

    display = None

    def __init__(self):

        self.display = SH1107(
            self.display_bus, 
            width=self.WIDTH, 
            height=self.HEIGHT,
            display_offset=DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297
        )
        self.group = displayio.Group()

    def show(self, file_path):
        bitmap = displayio.OnDiskBitmap(file_path)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        # Add the TileGrid to the Group
        self.group.append(tile_grid)

        # Add the Group to the Display
        self.display.root_group = self.group

    def turn_off(self):
        bitmap = displayio.Bitmap(self.WIDTH, self.HEIGHT, 1)
        palette = displayio.Palette(1)
        palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            bitmap, pixel_shader=palette, x=self.BORDER, y=self.BORDER
        )
        
        self.group.append(inner_sprite)
            
        