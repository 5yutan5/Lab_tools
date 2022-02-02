from __future__ import annotations

from serial import Serial


class _ArduinoSerial(Serial):
    def __init__(self) -> None:
        super().__init__(timeout=10)
        self._delimiter = "\r\n"

    def send_message(self, message: str) -> None:
        self.write(bytes(message + self._delimiter, "utf-8"))

    def receive_message(self) -> str:
        return (self.readline()[: -1 * len(self._delimiter)]).decode("utf-8")


class HighVoltageController:
    """Controller class for high voltage circuit."""

    PORT_FILTER = ""

    def __init__(self) -> None:
        """Initialize device class."""
        super().__init__()
        self._ser = _ArduinoSerial()
        self.port = ""
        self.baudrate = 0

    def open(self) -> None:
        """Open device."""
        self._ser.port = self.port
        self._ser.baudrate = self.baudrate
        self._ser.timeout = 0.1
        self._ser.open()

    def close(self) -> None:
        """Close device."""
        if self._ser.is_open:
            pass
        self._ser.close()

    def send(self, message: str) -> None:
        """Send message to device."""
        self._ser.send_message(message)

    def send_query_message(self, message: str) -> str:
        """Send query message."""
        self._ser.send_message(message)
        return self._ser.receive_message()
