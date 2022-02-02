import json
from importlib import resources
from pathlib import Path

import qtawesome as qta
from diy_hv._device import HighVoltageController
from diy_hv._widgets import FlexiblePopupCombobox, PortCombobox
from qtpy.QtCore import Slot  # type: ignore
from qtpy.QtGui import QAction
from qtpy.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from serial import SerialException


class MainWindowUI:
    """UI for mainwindow."""

    def setup_ui(self, main_win: QDialog) -> None:
        """Setup method for ui."""
        # Actions
        self.action_connect = QAction("Connect")
        self.action_disconnect = QAction("Disconnect")
        self.action_update_command = QAction("Update command")
        self.action_register_user_file = QAction("Register user file")

        # Widgets
        self.tool_btn_connection = QToolButton()
        self.push_btn_static = QPushButton("Static")
        self.push_btn_dynamic = QPushButton("Dynamic")
        self.stack_widget = QStackedWidget()
        self.combo_static_voltage = FlexiblePopupCombobox()
        self.combo_dynamic_voltage = FlexiblePopupCombobox()
        self.combo_dynamic_frequency = FlexiblePopupCombobox()
        self.push_btn_send = QPushButton("Send command")
        self.push_btn_stop = QPushButton("Stop")

        menubar = QMenuBar()

        # Setup widgets
        self.tool_btn_connection.setDefaultAction(self.action_connect)
        self.push_btn_static.setCheckable(True)
        self.push_btn_dynamic.setCheckable(True)
        btn_group_menu = QButtonGroup(main_win)
        btn_group_menu.addButton(self.push_btn_static)
        btn_group_menu.addButton(self.push_btn_dynamic)
        btn_group_menu.setExclusive(True)
        self.push_btn_static.setChecked(True)
        self.push_btn_send.setDefault(True)
        self.push_btn_send.setContentsMargins(12, 0, 12, 12)
        for btn in (self.push_btn_static, self.push_btn_dynamic, self.push_btn_stop):
            btn.setAutoDefault(False)

        menu_connection = menubar.addMenu("&Connection")
        menu_connection.addActions((self.action_connect, self.action_disconnect))
        menu_setting = menubar.addMenu("&Setting")
        menu_setting.addAction(self.action_register_user_file)

        # Layout
        static_page = QWidget()
        static_layout = QFormLayout(static_page)
        static_layout.addRow("Voltage", self.combo_static_voltage)
        dynamic_page = QWidget()
        dynamic_layout = QFormLayout(dynamic_page)
        dynamic_layout.addRow("Voltage", self.combo_dynamic_voltage)
        dynamic_layout.addRow("Frequency", self.combo_dynamic_frequency)
        self.stack_widget.addWidget(static_page)
        self.stack_widget.addWidget(dynamic_page)

        mode_layout = QHBoxLayout()
        mode_layout.setContentsMargins(12, 12, 12, 0)
        mode_layout.addWidget(self.tool_btn_connection)
        mode_layout.addWidget(self.push_btn_static)
        mode_layout.addWidget(self.push_btn_dynamic)

        default_btn_layout = QHBoxLayout()
        default_btn_layout.setContentsMargins(12, 0, 12, 12)
        default_btn_layout.addWidget(self.push_btn_stop)
        default_btn_layout.addWidget(self.push_btn_send)

        main_layout = QVBoxLayout(main_win)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(mode_layout)
        main_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))  # type: ignore
        main_layout.addWidget(self.stack_widget)
        main_layout.addLayout(default_btn_layout)

        main_layout.setMenuBar(menubar)


class DeviceDialog(QDialog):
    """Device dialog."""

    def __init__(self, device: HighVoltageController) -> None:
        """Initialize dialog."""
        super().__init__()
        self._device = device
        self._baudrate_combo = FlexiblePopupCombobox()
        self._port_combo = PortCombobox()
        self._btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self._setup_ui()

    def _setup_ui(self) -> None:
        # Setup ui
        self._baudrate_combo.addItems(("2400", "4800", "9600", "14400", "19200", "28800"))
        self._baudrate_combo.setCurrentText("9600")
        self._btn_box.button(QDialogButtonBox.StandardButton.Ok).setText("Connect")
        self._btn_box.button(QDialogButtonBox.StandardButton.Ok).pressed.connect(self._connect)
        self._btn_box.button(QDialogButtonBox.StandardButton.Cancel).pressed.connect(self.reject)
        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._baudrate_combo)
        main_layout.addWidget(self._port_combo)
        main_layout.addWidget(self._btn_box)

    @Slot()
    def _connect(self) -> None:
        self._device.baudrate = int(self._baudrate_combo.currentText())
        port_info = self._port_combo.get_select_port_info()
        if port_info is None:
            QMessageBox.warning(self, "Warning", "Port is not selected.")
            return
        self._device.port = port_info.device
        try:
            self._device.open()
        except SerialException:
            self.reject()
        self.accept()


class MainWindow(QDialog):
    """Main window for app."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self._ui = MainWindowUI()
        self._ui.setup_ui(self)
        self._device = HighVoltageController()
        self._command_conf: dict[str, list[dict[str, str | int]]] = {}

        # Signal
        QApplication.instance().paletteChanged.connect(self._sync_theme_with_system)  # type: ignore
        for btn in (self._ui.push_btn_static, self._ui.push_btn_dynamic):
            btn.pressed.connect(self._switch_mode)
        for action in (self._ui.action_connect, self._ui.action_disconnect):
            action.triggered.connect(self._toggle_connection)
        self._ui.push_btn_send.pressed.connect(self._send_command)
        self._ui.action_register_user_file.triggered.connect(self._register_user_command)

        # Setup window
        self._sync_theme_with_system()
        self._ui.action_disconnect.trigger()
        self._update_command()
        self.setWindowTitle("DIYHV")

    @Slot()
    def _sync_theme_with_system(self) -> None:
        import darkdetect
        import qdarktheme

        try:
            theme = darkdetect.theme()
            if theme is None:
                theme = "dark"
        except FileNotFoundError:
            theme = "dark"
        theme = theme.lower()

        app: QApplication = QApplication.instance()  # type: ignore
        app.setPalette(qdarktheme.load_palette(theme))
        app.setStyleSheet(qdarktheme.load_stylesheet(theme))
        icon_color = app.palette().text().color()
        window_color = app.palette().window().color()

        # Update icon
        self._ui.action_connect.setIcon(qta.icon("mdi6.power-plug", color=icon_color))
        self._ui.action_disconnect.setIcon(qta.icon("mdi6.power-plug-off", color=icon_color))
        self._ui.action_update_command.setIcon(qta.icon("mdi6.file-cog-outline", color=icon_color))
        self._ui.push_btn_send.setIcon(qta.icon("mdi6.send", color=window_color))
        self._ui.action_register_user_file.setIcon(qta.icon("mdi.content-save-cog", color=icon_color))

    @Slot()
    def _switch_mode(self) -> None:
        mode: str = self.sender().text()  # type: ignore
        self._ui.stack_widget.setCurrentIndex(0 if mode == "Static" else 1)

    @Slot()
    def _toggle_connection(self) -> None:
        connection: str = self.sender().text()  # type: ignore
        is_connect = connection == "Connect"
        if is_connect:
            result = DeviceDialog(self._device).exec()
            if result == 0:
                return
            self._ui.tool_btn_connection.setDefaultAction(self._ui.action_disconnect)
            self._ui.tool_btn_connection.removeAction(self._ui.action_connect)
        else:
            self._device.close()
            self._ui.tool_btn_connection.setDefaultAction(self._ui.action_connect)
            self._ui.tool_btn_connection.removeAction(self._ui.action_disconnect)
        self._ui.push_btn_send.setEnabled(is_connect)
        self._ui.action_connect.setDisabled(is_connect)
        self._ui.action_disconnect.setEnabled(is_connect)
        self._ui.push_btn_stop.setEnabled(is_connect)

    @Slot()
    def _update_command(self, user_command_conf: dict = None) -> None:
        with resources.path("diy_hv", "default.json") as path:
            json_text = path.read_bytes()
        command_conf: dict = json.loads(json_text)
        if user_command_conf is not None:
            command_conf.update(user_command_conf)
        stop_command: str = command_conf.pop("stop")
        self._command_conf = command_conf
        static_commands: list[dict[str, str | int]] = command_conf["static"]
        dynamic_commands: list[dict[str, str | int]] = command_conf["dynamic"]

        # Static
        self._ui.combo_static_voltage.clear()
        static_voltages = {str(command["voltage"]) for command in static_commands}
        self._ui.combo_static_voltage.addItems(sorted(static_voltages))

        # Dynamic
        self._ui.combo_dynamic_voltage.clear()
        self._ui.combo_dynamic_frequency.clear()
        dynamic_voltages = {str(command["voltage"]) for command in dynamic_commands}
        dynamic_frequency = {str(command["frequency"]) for command in dynamic_commands}
        self._ui.combo_dynamic_voltage.addItems(sorted(dynamic_voltages))
        self._ui.combo_dynamic_frequency.addItems(sorted(dynamic_frequency))

        self._ui.push_btn_stop.disconnect()
        self._ui.push_btn_stop.pressed.connect(lambda: self._device.send(stop_command))

    @Slot()
    def _register_user_command(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, "Open File", filter="Settings (*.json)")[0]
        if file_name == "":
            return
        path = Path(file_name).absolute()
        json_text = path.read_bytes()
        user_conf = json.loads(json_text)
        self._update_command(user_conf)

    @Slot()
    def _send_command(self) -> None:
        is_static = self._ui.push_btn_static.isChecked()
        if is_static:
            for command in self._command_conf["static"]:
                voltage = self._ui.combo_static_voltage.currentText()
                if str(command["voltage"]) == voltage:
                    command = command["command"]
                    break
            else:
                QMessageBox.warning(self, "Warning", "Command not found.")
                return
        else:
            for command in self._command_conf["dynamic"]:
                voltage = self._ui.combo_dynamic_voltage.currentText()
                frequency = self._ui.combo_dynamic_frequency.currentText()
                if str(command["voltage"]) == voltage and str(command["frequency"]) == frequency:
                    command = command["command"]
                    break
            else:
                QMessageBox.warning(self, "Warning", "Command not found.")
                return
        self._device.send(command)  # type: ignore
