import sys
import datetime as dt

from PySide6 import QtWidgets, QtGui, QtCore

from db import Database
from alarm import Alarm
from janela_nova import TimerWindow


def check_alarms() -> None:
    """Checks alarms and display notification."""

    now = dt.datetime.now()
    alarms = [Alarm(t[0], t[1], t[2], t[3]) for t in Database().alarms]
    for alarm in alarms:
        hour = alarm.hour
        minutes = alarm.minutes
        description = alarm.description
        if hour == now.hour and minutes == now.minute:
            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Icon.Information)
            aviso.setWindowTitle(f"Alarme {hour:02}:{minutes:02}")
            aviso.setText(description)
            aviso.exec()


def main() -> None:
    """Program start"""

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Timer
    timer = QtCore.QTimer()
    timer.start(1000 * 31)
    timer.timeout.connect(check_alarms)

    # Main window
    window = TimerWindow()

    # System tray
    tray = QtWidgets.QSystemTrayIcon()
    icon = QtGui.QIcon("icone.ico")
    tray.setIcon(icon)
    tray.setVisible(True)

    # Tray menu
    menu = QtWidgets.QMenu()
    open_window = QtGui.QAction("Verificar alarmes")
    open_window.triggered.connect(window.show)
    menu.addAction(open_window)
    close_app = QtGui.QAction("Fechar")
    close_app.triggered.connect(app.quit)
    menu.addAction(close_app)
    tray.setContextMenu(menu)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
