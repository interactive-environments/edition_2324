# wifi_setup.py
from digitalio import DigitalInOut
import board
import busio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

class WiFi():

    def __init__(self):
        # Get wifi details from settings.py
        try:
            from settings import settings
        except ImportError:
            print("WiFi settings are kept in settings.py, please add or change them there!")
            raise

        # Connect to the WiFi chip on the Bitsy Expander
        esp32_cs = DigitalInOut(board.D9)               # Chip select pin
        esp32_ready = DigitalInOut(board.D11)           # BUSY or READY pin
        esp32_reset = DigitalInOut(board.D12)           # Reset pin
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        # Create wifi object
        self.wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(self.esp, settings)

        # Connect to WiFi
        print("Connecting to WiFi...")
        self.wifi.connect()
        print("Connected!")
