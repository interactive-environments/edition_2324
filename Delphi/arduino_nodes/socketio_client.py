import struct
import os
import json
import binascii
import random
import adafruit_esp32spi.adafruit_esp32spi_socket as socket


OPCODE_CONTINUATION = 0x00
OPCODE_TEXT = 0x01
OPCODE_BINARY = 0x02
OPCODE_CONNECTION_CLOSE = 0x08
OPCODE_PING = 0x09
OPCODE_PONG = 0x0A

OPCODE_FIN_CONTINUATION = 0x80
OPCODE_FIN_TEXT = 0x81
OPCODE_FIN_BINARY = 0x82
OPCODE_FIN_CONNECTION_CLOSE = 0x88
OPCODE_FIN_PING = 0x89
OPCODE_FIN_PONG = 0x8A

SOCKET_OPEN = 0
SOCKET_CLOSE = 1
SOCKET_PING = 2
SOCKET_PONG = 3
SOCKET_MESSAGE_CONNECT = 40
SOCKET_MESSAGE_DISCONNECT = 41
SOCKET_MESSAGE_EVENT = 42
SOCKET_MESSAGE_ACK = 43
SOCKET_MESSAGE_CONNECT_ERROR = 44
SOCKET_MESSAGE_BINARY_EVENT = 45
SOCKET_MESSAGE_BINARY_ACK = 46
SOCKET_UPGRADE = 5
SOCKET_NOOP = 6

PACKET_TYPES = [
    SOCKET_OPEN,
    SOCKET_CLOSE,
    SOCKET_PING,
    SOCKET_PONG,
    SOCKET_MESSAGE_CONNECT,
    SOCKET_MESSAGE_DISCONNECT,
    SOCKET_MESSAGE_EVENT,
    SOCKET_MESSAGE_ACK,
    SOCKET_MESSAGE_CONNECT_ERROR,
    SOCKET_MESSAGE_BINARY_EVENT,
    SOCKET_MESSAGE_BINARY_ACK,
    SOCKET_UPGRADE,
    SOCKET_NOOP,
]


class SocketIOClient:
    def __init__(self, esp, _HOST, _PORT, debug=False):
        self._esp = esp
        self._s = None

        self._transport = "polling"

        self._sid = None
        self._pingInterval = None
        self._pingTimeout = None
        self._maxPayload = None

        self._event_handlers = {}
        self._debug = debug

        self._HOST = _HOST
        self._PORT = _PORT

    def reset(self):
        self._s = None

        self._transport = "polling"

        self._sid = None
        self._pingInterval = None
        self._pingTimeout = None
        self._maxPayload = None

    def is_connected(self):
        if not self._s:
            return False
        return self._s._connected()

    def _generate_masking_key(self):
        # Generate a random 32-bit integer as the masking key
        return struct.pack(">I", random.getrandbits(32))

    def _apply_mask(self, payload, masking_key):
        # XOR each byte of the payload with the corresponding byte of the masking key
        masked_payload = bytearray()
        for i in range(len(payload)):
            masked_payload.append(payload[i] ^ masking_key[i % 4])
        return masked_payload

    def _encode_payload_length(self, length):
        if length < 126:
            return struct.pack("!B", 0x80 | length)
        elif length < 65536:
            return struct.pack("!BBH", 0x80 | 126, (length >> 8) & 0xFF, length & 0xFF)
        else:
            return struct.pack("!BQ", 0x80 | 127, length)

    def _create_frame(self, opcode, payload=b""):
        frame = bytearray([opcode])
        frame.extend(self._encode_payload_length(len(payload)))
        masking_key = self._generate_masking_key()
        frame.extend(masking_key)
        frame.extend(self._apply_mask(payload, masking_key))
        return bytes(frame)

    def _generate_websocket_key(self):
        # Generate a 16-byte random key
        random_key = os.urandom(16)
        # Encode the key to base64 as required by the WebSocket protocol
        websocket_key = binascii.b2a_base64(random_key)[:-1].decode("utf-8")
        return websocket_key

    def _upgrade(self):
        # Perform the Socket.IO WebSocket handshake
        if self._debug:
            print("Upgrading to WebSocket...")
        # Generate a unique WebSocket key for each handshake
        websocket_key = self._generate_websocket_key()

        if self._debug:
            print(f"WebSocket Key: {websocket_key}")
        # Construct the upgrade request
        # Send Socket.IO handshake request using the stored host and path
        upgrade_request = (
            "GET /socket.io/?EIO=4&transport=websocket&sid={} HTTP/1.1\r\n"
            "Host: {}:{}\r\n"
            "Connection: Upgrade\r\n"
            "Upgrade: websocket\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Sec-WebSocket-Key: {}\r\n"
            "\r\n"
        ).format(self._sid, self._HOST, self._PORT, websocket_key)
        self._s.send(upgrade_request.encode("utf-8"))

        # Receive and process the WebSocket upgrade response
        upgrade_response = self._s.recv(1024).decode("utf-8")
        if self._debug:
            print("Received response from WebSocket upgrade:")
            print(upgrade_response)

        # Send ping frame with payload 'probe'
        ping_frame = self._create_frame(OPCODE_FIN_TEXT, b"2probe")
        self._s.send(ping_frame)

        # Handle the pong frame and check if it contains the expected payload 'probe'
        _, payload = self._read_frame()
        if payload != b"3probe":
            raise ConnectionError("Invalid probe response")

        # Send upgrade frame
        upgrade_frame = self._create_frame(OPCODE_FIN_TEXT, b"5")
        self._s.send(upgrade_frame)

        self._transport = "websocket"
        if self._debug:
            print("WebSocket upgrade successful")

    def _handshake(self):
        # Construct and send the Socket.IO handshake request
        handshake_request = (
            "GET /socket.io/?EIO=4&transport=polling HTTP/1.1\r\n"
            "Host: {}:{}\r\n"
            "\r\n"
        ).format(self._HOST, self._PORT)
        self._s.send(handshake_request.encode("utf-8"))

        # Receive and process the initial response
        handshake_response = self._s.recv(1024).decode("utf-8")
        if self._debug:
            print("Received response from polling transport:")
            print(handshake_response)

        payload_start = handshake_response.find("\r\n\r\n") + 5
        response_json = None
        try:
            response_json = json.loads(handshake_response[payload_start:])
        except ValueError as e:
            print("Error parsing JSON from handshake response:", e)
            raise e
        if response_json is not None:
            self._sid = response_json.get("sid")
            self._pingInterval = response_json.get("pingInterval", 25000)
            self._pingTimeout = response_json.get("pingTimeout", 20000)
            self._maxPayload = response_json.get("maxPayload", 1000000)
            upgrades = response_json.get("upgrades", [])
            if self._debug:
                print(f"Extracted SID: {self._sid}")
                print(f"Extracted ping interval: {self._pingInterval}")
                print(f"Extracted ping timeout: {self._pingTimeout}")
                print(f"Extracted max payload: {self._maxPayload}")

        # Connect
        connection_request = (
            "POST /socket.io/?EIO=4&transport={}&sid={} HTTP/1.1\r\n"
            "Host: {}:{}\r\n"
            "Content-Length: 2\r\n"
            "Content-type: text/plain;charset=UTF-8\r\n"
            "\r\n"
            "40"
        ).format(self._transport, self._sid, self._HOST, self._PORT)
        self._s.send(connection_request.encode("utf-8"))

        # Receive and process the connection response
        connection_response = self._s.recv(1024).decode("utf-8")
        if self._debug:
            print("Received response:")
            print(connection_response)
        if "Bad Request" in connection_response:
            self.reset()
            return

        # Upgrade to websocket if possible
        if upgrades and "websocket" in upgrades:
            self._upgrade()

    def _read_frame(self):
        # Read the first 2 bytes to get frame header
        header = self._s.recv(2)

        # Extract relevant information from the frame header
        fin = header[0] & 0x80
        opcode = header[0] & 0x0F
        payload_length = header[1] & 0x7F

        # Determine if the payload length is extended (126 or 127)
        if payload_length == 126:
            # Read the next 2 bytes for a 16-bit unsigned integer
            extended_payload_length = int.from_bytes(self._s.recv(2), "big")
        elif payload_length == 127:
            # Read the next 8 bytes for a 64-bit unsigned integer
            extended_payload_length = int.from_bytes(self._s.recv(8), "big")
        else:
            extended_payload_length = None

        # Calculate the actual payload length
        if extended_payload_length is not None:
            payload_length = extended_payload_length

        payload = self._s.recv(payload_length)

        # If this is a continuation frame, read additional frames until FIN is set
        while not fin:
            # Read the next frame header
            next_header = socket.recv(2)

            # Extract FIN, Opcode, and Payload Length information from the next header
            fin = next_header[0] & 0x80
            # next_opcode = next_header[0] & 0x0F
            next_payload_length = next_header[1] & 0x7F

            # Read the next payload data based on the next payload length
            next_payload_data = socket.recv(next_payload_length)

            # Concatenate the payload data with the previous payload
            payload += next_payload_data

        return opcode, payload

    def _unmask_payload(self, masking_key, payload):
        # Unmask the payload using the masking key
        unmasked_payload = bytearray(payload)
        for i in range(len(payload)):
            unmasked_payload[i] = payload[i] ^ masking_key[i % 4]
        return bytes(unmasked_payload)

    def _unpack_payload(self, payload):
        if len(payload) < 1 or not payload[0].isdigit():
            raise OSError("Invalid payload")

        index = 1
        packet_type = int(payload[:index])
        num_binary_attachments = None
        namespace = None
        acknowledgement_id = None
        payload_data = None
        binary_attachments = None

        if packet_type == 4:
            index += 1
            packet_type = int(payload[:index])
        if packet_type not in PACKET_TYPES:
            raise OSError("Invalid packet type in payload")

        if index < len(payload) and payload[index].isdigit():
            start_index = index
            while payload[index].isdigit():
                index += 1
                if not index < len(payload):
                    raise OSError("Invalid packet format")
            if payload[index] == "-":
                num_binary_attachments = payload[start_index:index]
                index += 1
            else:
                index = start_index

        if index < len(payload) and payload[index] == "/":
            start_index = index
            while payload[index] != ",":
                index += 1
                if not index > len(payload):
                    raise OSError("Invalid packet format")
            namespace = payload[start_index:index]
            index += 1

        if index < len(payload) and payload[index].isdigit():
            start_index = index
            while payload[index].isdigit():
                index += 1
                if not index < len(payload):
                    raise OSError("Invalid packet format")
            acknowledgement_id = int(payload[start_index:index])
            index += 1

        if index < len(payload) and payload[index] != "\r\n":
            start_index = index
            while index < len(payload) and payload[index] != "\r\n":
                index += 1
            payload_data = payload[start_index:index]
            index += 1

        index += 1
        if index < len(payload):
            binary_attachments = payload[index : len(payload)].split("\r\n")

        return (
            packet_type,
            num_binary_attachments,
            namespace,
            acknowledgement_id,
            payload_data,
            binary_attachments,
        )

    def _handle_text_frame(self, payload):
        (
            packet_type,
            num_binary_attachments,
            namespace,
            acknowledgement_id,
            payload_data,
            binary_attachments,
        ) = self._unpack_payload(payload.decode())
        if packet_type == SOCKET_OPEN:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_CLOSE:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_PING:
            if self._debug:
                print("Received PING, sending PONG")

            pong_frame = self._create_frame(OPCODE_FIN_TEXT, str(SOCKET_PONG).encode())
            self._s.send(pong_frame)
        elif packet_type == SOCKET_PONG:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_MESSAGE_CONNECT:
            if self._debug:
                print("SocketIO connected")

        elif packet_type == SOCKET_MESSAGE_DISCONNECT:
            if self._debug:
                print("SocketIO disconnected")

            self.disconnect()
        elif packet_type == SOCKET_MESSAGE_EVENT:
            arr = json.loads(payload_data)

            if self._debug:
                print("Received event:", arr[0])

            self._invoke_event_handler(arr[0], arr[1] if len(arr) > 1 else None)
        elif packet_type == SOCKET_MESSAGE_ACK:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_MESSAGE_CONNECT_ERROR:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_MESSAGE_BINARY_EVENT:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_MESSAGE_BINARY_ACK:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_UPGRADE:
            raise NotImplementedError("Not yet implemented:", payload)
        elif packet_type == SOCKET_NOOP:
            raise NotImplementedError("Not yet implemented:", payload)

    def _handle_frame(self, opcode, payload):
        if opcode == 1:
            self._handle_text_frame(payload)
        elif opcode == 8:
            self.disconnect()
        else:
            print("Unhandled OPCODE in frame:", opcode)

    def _invoke_event_handler(self, event_name, event_data):
        # Invoke the registered event handler for the given event
        handler = self._event_handlers.get(event_name)
        if handler:
            handler(event_data)

    def on(self, event_name, handler):
        # Register an event handler for a specific event
        self._event_handlers[event_name] = handler

    def emit(self, event, data):
        try:
            payload_json = json.dumps([event, data])
            payload = "42{}".format(payload_json).encode()
            frame = self._create_frame(OPCODE_FIN_TEXT, payload)
            self._s.send(frame)
        except Exception as e:
            print("Not connected:", e)
            self.disconnect()

    def connect(self):
        # Connect to the WiFi network
        if not self._esp.is_connected:
            raise ConnectionError("ESP not connected")
        # Connect to the server
        addr = socket.getaddrinfo(self._HOST, self._PORT)[0][4]
        self._s = socket.socket()
        try:
            self._s.connect(addr)
            self._handshake()

        except TimeoutError as e:
            self.disconnect()
            print("Connection requets timed out:", e)
            raise e

    def disconnect(self):
        if self._s:
            self._s.close()
            self._s = None

    def loop(self):
        if self._s and self._s._connected():
            if self._s._available() > 0:
                opcode, payload = self._read_frame()
                self._handle_frame(opcode, payload)
