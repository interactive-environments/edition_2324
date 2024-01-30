from lib.lcd.lcd import LCD as LCD_class
from lib.lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import board
import time

display_full_block = (0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F)
display_empty_block = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

display_decreasing_blocks = [
    (0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F),
    (0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E),
    (0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C),
    (0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18),
    (0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10)
]

class LCD:

    lcd = None

    def __init__(self):
        self.lcd = LCD_class(I2CPCF8574Interface(board.I2C(), 0x3f), num_rows=2, num_cols=16) #if address 0x27 doesn't work use 0x3f
        self.lcd.set_cursor_pos(0,0)
        self.lcd.clear()
        self.lcd.set_backlight(True)

    def lcd_print_progress_bar(self, minutes):
        self.lcd.create_char(0, display_full_block)     # Creates custom charachter with all pixels ON at address 0
        self.lcd.create_char(1, display_empty_block)    # Creates custom charachter with all pixels OFF at address 1

        interval = minutes * 60 / 80    # Calculates the interval between each update based on the break time

        # Fill second row with fully lighted pixels
        for i in range(self.lcd.num_cols):
            self.lcd.set_cursor_pos(1, i)   
            self.lcd.write(0)

        # Starting from the last square, update the progress bar
        for index in range(self.lcd.num_cols - 1, -1, -1):
            for block in display_decreasing_blocks:
                self.lcd.set_cursor_pos(1, index)
                self.lcd.create_char(2, block)
                self.lcd.write(2)
                time.sleep(interval)
            self.lcd.set_cursor_pos(1, index)
            self.lcd.write(1)
        
        self.lcd.clear()
        self.lcd.print('Go take a break in the game area')

    def  print(self, str):
        self.lcd.print(str)

    def clear(self):
        self.lcd.clear()