import board
import asyncio
import busio


class RFID:

    rfid = None

    def __init__(self):
        self.rfid = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.05)

    def get_data(self):
        return self.rfid.read(14)

		# will look something like this:
		# b'\x023B00770095D9\x03'
		# every card has a unique ID, so you can check if a specific card was scanned
		# if data == b'\x023B00770095D9\x03':