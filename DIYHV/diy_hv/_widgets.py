import platform

from qtpy.QtCore import QEvent, QModelIndex, QObject, Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QComboBox, QStyledItemDelegate, QWidget
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo


class FlexiblePopupCombobox(QComboBox):
    """Flexible combobox."""

    class _MouseWheelGuard(QObject):
        def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
            if platform.system() == "Darwin":
                if event.type() == QEvent.Type.Wheel and not watched.hasFocus():  # type: ignore
                    event.ignore()
                    return True
                return False
            elif platform.system() == "Windows":
                if event.type() == QEvent.Type.Wheel:
                    event.ignore()
                    return True
                return False
            return super().eventFilter(watched, event)

    def __init__(self, parent: QWidget = None, enable_auto_wheel_focus: bool = True) -> None:
        """Initialize class."""
        super().__init__(parent=parent)
        delegate = QStyledItemDelegate(parent)
        if enable_auto_wheel_focus:
            self.installEventFilter(self._MouseWheelGuard(self))
        self.setItemDelegate(delegate)

    def showPopup(self) -> None:  # noqa: N802
        """Override method."""
        width = self.view().sizeHintForColumn(0) + 20
        self.view().setMinimumWidth(width)
        super().showPopup()


def _search_ports(filter: str) -> list[ListPortInfo]:
    return [port for port in list_ports.comports() if filter in str(port.description)]


class PortCombobox(FlexiblePopupCombobox):
    """Port combobox."""

    class _KeyEventGuard(QObject):
        def __init__(self, parent: QComboBox) -> None:
            super().__init__(parent=parent)
            self._combobox = parent

        def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
            if type(event) is QKeyEvent:
                if event.key() in [Qt.Key.Key_Return, Qt.Key.Key_Enter]:
                    self._combobox.view().pressed.emit(self._combobox.view().currentIndex())
                    event.ignore()
                    return True
                return False
            return super().eventFilter(watched, event)

    def __init__(self, filter: str = None, parent: QWidget = None):
        """Initialize class."""
        super().__init__(parent=parent)
        self._port_infos = []
        self.filter = "" if filter is None else filter
        self._port_selected = None

        self.setPlaceholderText("Select Port")
        self.view().pressed.connect(self._handle_item_pressed)
        self.view().installEventFilter(self._KeyEventGuard(self))

    def get_select_port_info(self) -> ListPortInfo | None:
        """Get select port info."""
        return self._port_selected

    def showPopup(self) -> None:  # noqa: N802
        """Override method."""
        self._port_infos.clear()
        current_text = self.currentText()
        self.clear()
        self._port_infos = _search_ports(self.filter)
        for port in self._port_infos:
            description = port.device
            if port.manufacturer is not None:
                description += f"  |  {port.manufacturer}"
            self.addItem(description)
            if current_text != "" and current_text in description:
                self.setCurrentText(description)

        if len(self._port_infos) == 0:
            self._port_selected = None

        port_selected = self._port_selected
        if port_selected is not None:
            if port_selected.manufacturer is None:
                self.setCurrentText(f"{port_selected.device}")
            else:
                self.setCurrentText(f"{port_selected.device}  |  {port_selected.manufacturer}")
        super().showPopup()

    def _handle_item_pressed(self, index: QModelIndex) -> None:
        self._port_selected = self._port_infos[index.row()]
