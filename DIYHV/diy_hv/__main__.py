"""Module allowing for `python -m control_high_voltage.gui`."""
import sys

from diy_hv._mainwindow import MainWindow
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore
    win = MainWindow()
    win.show()
    app.exec()
