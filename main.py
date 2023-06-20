import sys
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore

from db import Database
from main_window import TimerWindow


def check_alarms() -> None:
    """Checks alarms and display notification."""

    now = datetime.now()
    alarms = Database().list_alarms()
    for alarm in alarms:
        alarm_ringed = alarm.next_alarm > now
        if not alarm_ringed:
            next_alarm = alarm.next_alarm + timedelta(days=1)
            Database().ring_alarm(alarm.id, next_alarm=next_alarm)

            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Icon.Information)
            aviso.setWindowTitle(f"Alarm {alarm.next_alarm.hour:02}:{alarm.next_alarm.minute:02}")
            aviso.setText(alarm.description)
            aviso.exec()


def main() -> None:
    """Program start"""

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Timer
    timer = QtCore.QTimer()
    timer.start(1000)  # Timer timeout every second
    timer.timeout.connect(check_alarms)

    # Main window
    window = TimerWindow()

    # System tray
    tray = QtWidgets.QSystemTrayIcon()
    icon = QtGui.QIcon("icon.ico")
    tray.setIcon(icon)
    tray.setVisible(True)

    # Tray menu
    menu = QtWidgets.QMenu()
    open_window = QtGui.QAction("Show alarms")
    open_window.triggered.connect(window.show)
    menu.addAction(open_window)
    close_app = QtGui.QAction("Quit")
    close_app.triggered.connect(app.quit)
    menu.addAction(close_app)
    tray.setContextMenu(menu)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
