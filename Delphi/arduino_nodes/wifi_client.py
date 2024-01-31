from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_requests as requests


class WiFiClient:
    def __init__(self, esp, secrets, status_pixel=None, attempts=2, debug=False):
        self.esp = esp
        requests.set_socket(socket, esp)
        self._debug = debug
        self._ssid = secrets["ssid"]
        self._password = secrets.get("password", None)
        self._attempts = attempts
        self._statuspix = status_pixel
        self.pixel_status((100, 0, 0))
        self._ap_index = 0

    def _get_next_ap(self):
        if isinstance(self._ssid, (tuple, list)) and isinstance(
            self._password, (tuple, list)
        ):
            if not self._ssid or not self._password:
                raise ValueError("SSID and Password should contain at least 1 value")
            if len(self._ssid) != len(self._password):
                raise ValueError("The length of SSIDs and Passwords should match")
            access_point = (self._ssid[self._ap_index], self._password[self._ap_index])
            self._ap_index += 1
            if self._ap_index >= len(self._ssid):
                self._ap_index = 0
            return access_point
        if isinstance(self._ssid, (tuple, list)) or isinstance(
            self._password, (tuple, list)
        ):
            raise NotImplementedError(
                "If using multiple passwords, both SSID"
                "and Password should be lists or tuples"
            )
        return (self._ssid, self._password)

    def get_ap_length(self):
        if isinstance(self._ssid, (tuple, list)) and isinstance(
            self._password, (tuple, list)
        ):
            if not self._ssid or not self._password:
                raise ValueError("SSID and Password should contain at least 1 value")
            if len(self._ssid) != len(self._password):
                raise ValueError("The length of SSIDs and Passwords should match")
            return len(self._ssid)
        if isinstance(self._ssid, (tuple, list)) or isinstance(
            self._password, (tuple, list)
        ):
            raise NotImplementedError(
                "If using multiple passwords, both SSID"
                "and Password should be lists or tuples"
            )
        return 1

    def reset(self):
        if self._debug:
            print("Resetting ESP32")
        self.esp.reset()

    def is_connected(self):
        return self.esp.is_connected

    def connect(self):
        if self._debug:
            if self.esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
                print("ESP32 found and in idle mode")
            print("Firmware vers.", self.esp.firmware_version.decode("utf-8"))
            print(
                "MAC addr:",
                ":".join([("%02x" % byte) for byte in self.esp.MAC_address]),
            )
            for access_pt in self.esp.scan_networks():
                print(
                    "\t%s\t\tRSSI: %d"
                    % (str(access_pt["ssid"], "utf-8"), access_pt["rssi"])
                )
        failure_count = 0
        (ssid, password) = self._get_next_ap()
        for _ in range(self.get_ap_length() * self._attempts):
            try:
                if self._debug:
                    print("Connecting to AP...")
                self.pixel_status((100, 50, 0))
                self.esp.connect_AP(
                    bytes(ssid, "utf-8"), bytes(password, "utf-8"), timeout_s=5
                )
                failure_count = 0
                self.pixel_status((0, 100, 0))
                if self._debug:
                    print(
                        "Connected to",
                        str(self.esp.ssid, "utf-8"),
                        "\tRSSI:",
                        self.esp.rssi,
                    )
                    print("My IP address is", self.esp.pretty_ip(self.esp.ip_address))
                return
            except OSError as error:
                print("Failed to connect, retrying\n", error)
                failure_count += 1
                if failure_count >= self._attempts:
                    failure_count = 0
                    (ssid, password) = self._get_next_ap()
                continue
        self.reset()
        self.pixel_status((100, 0, 0))

    def get(self, url, **kw):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.get(url, **kw)
        self.pixel_status((0, 100, 0))
        return return_val

    def post(self, url, **kw):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.post(url, **kw)
        self.pixel_status((0, 100, 0))
        return return_val

    def put(self, url, **kw):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.put(url, **kw)
        self.pixel_status((0, 100, 0))
        return return_val

    def patch(self, url, **kw):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.patch(url, **kw)
        self.pixel_status((0, 100, 0))
        return return_val

    def delete(self, url, **kw):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        return_val = requests.delete(url, **kw)
        self.pixel_status((0, 100, 0))
        return return_val

    def ping(self, host, ttl=250):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        response_time = self.esp.ping(host, ttl=ttl)
        self.pixel_status((0, 100, 0))
        return response_time

    def ip_address(self):
        if not self.esp.is_connected:
            self.connect()
        self.pixel_status((0, 0, 100))
        self.pixel_status((0, 100, 0))
        return self.esp.pretty_ip(self.esp.ip_address)

    def pixel_status(self, value):
        if self._statuspix:
            if hasattr(self._statuspix, "color"):
                self._statuspix.color = value
            else:
                self._statuspix.fill(value)

    def signal_strength(self):
        if not self.esp.is_connected:
            self.connect()
        return self.esp.rssi
