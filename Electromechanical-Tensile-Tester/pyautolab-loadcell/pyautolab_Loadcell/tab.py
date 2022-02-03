"""Module for pyautolab tab."""
from __future__ import annotations

from pyautolab import api
from pyautolab_Loadcell.driver import PARAMETER, Loadcell


class TabLoadcell(api.DeviceTab):
    """Device tab for loadcell."""

    def __init__(self, device: Loadcell) -> None:
        """Initialize class."""
        super().__init__()
        self._ui = _TabUI()
        self._ui.setup_ui(self)
        self._ui._set_zero_button.clicked.connect(device.fix_zero)

    def get_parameters(self) -> dict[str, str]:
        """Override Device class."""
        return PARAMETER


class _TabUI:
    def setup_ui(self, parent) -> None:
        self._set_zero_button = api.qt_helpers.create_push_button(text="Fix Zero")
        api.qt_helpers.create_v_box_layout([self._set_zero_button], parent)
