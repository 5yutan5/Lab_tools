"""Module for device."""
from __future__ import annotations

import pyautolab.api as api
from serial import Serial

PARAMETER = {"Tension": "g"}


class _LoadcellSerial(Serial):
    def __init__(self) -> None:
        super().__init__(timeout=0)
        self._delimiter = "\r\n"

    def send_message(self, message: str) -> None:
        self.write(bytes(message + self._delimiter, "utf-8"))

    def receive_message(self) -> str:
        return self.readline().decode("utf-8").strip().rstrip()

    def send_query_message(self, message: str) -> str:
        self.send_message(message)
        return self.receive_message()


class Loadcell(api.Device):
    """Loadcell class."""

    PORT_FILTER = ""

    def __init__(self) -> None:
        """Initialize class."""
        super().__init__()
        self._ser = _LoadcellSerial()

    def open(self) -> None:
        """Override Device class."""
        self._ser.port = self.port
        self._ser.baudrate = self.baudrate
        self._ser.timeout = 0.1
        self._ser.open()

    def close(self) -> None:
        """Override Device class."""
        self._ser.close()

    def receive(self) -> str:
        """Override Device class."""
        return self._ser.receive_message()

    def send(self, message: str) -> None:
        """Override Device class."""
        self._ser.send_message(message)

    def reset_buffer(self) -> None:
        """Override Device class."""
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

    def measure(self) -> dict[str, float]:
        """Override Device class."""
        result = self._ser.send_query_message("a")
        return {list(PARAMETER)[0]: float(result)}

    def fix_zero(self) -> None:
        """Fix zero."""
        self._ser.send_message("b")
