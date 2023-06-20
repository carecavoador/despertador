from datetime import datetime
from PySide6 import QtWidgets, QtGui

from alarm import Alarm
from db import Database


class NewTimerDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Add alarm")

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.dialog_buttons = QtWidgets.QDialogButtonBox(buttons)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.label_time = QtWidgets.QLabel("New alarm time:")
        self.time = QtWidgets.QTimeEdit()
        self.label_desc = QtWidgets.QLabel("Alarm description:")
        self.description = QtWidgets.QLineEdit()

        self.layout.addWidget(self.label_time)
        self.layout.addWidget(self.time)
        self.layout.addWidget(self.label_desc)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.dialog_buttons)
        self.setLayout(self.layout)


class TimerWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Despertador 0.2.0")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setMinimumSize(240, 360)

        self.main_panel = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout(self.main_panel)

        self.btn_add = QtWidgets.QPushButton("Add alarm")
        self.btn_add.clicked.connect(self.add_timer)

        self.timers_panel = QtWidgets.QWidget()
        self.timers_layout = QtWidgets.QVBoxLayout(self.timers_panel)
        self.timers_layout.addStretch()
        self.timers_layout.setDirection(self.timers_layout.Direction.BottomToTop)

        self.main_layout.addWidget(self.btn_add, 0, 0)
        self.main_layout.addWidget(self.timers_panel, 1, 0)

        # DATA
        self.timers = []
        self.update_timers()
        for timer in self.timers:
            self.display_timer(timer)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(
            self.scroll.verticalScrollBarPolicy().ScrollBarAlwaysOn
        )
        self.scroll.setWidget(self.main_panel)
        self.setCentralWidget(self.scroll)

    def update_timers(self) -> None:
        self.timers = Database().list_alarms()

    def display_timer(self, timer: Alarm) -> None:
        def remove_from_layout(
            timer, layout: QtWidgets.QLayout, widget: QtWidgets.QWidget
        ) -> None:
            layout.removeWidget(widget)
            widget.deleteLater()
            self.remove_timer(timer)

        widget = QtWidgets.QGroupBox()
        layout = QtWidgets.QGridLayout(widget)

        label_description = QtWidgets.QLabel(f"<b>{timer.description}</b>")
        label_time = QtWidgets.QLabel(f"{timer.next_alarm.hour:02}:{timer.next_alarm.minute:02}")
        btn_remove = QtWidgets.QPushButton(text="Remove alarm")
        btn_remove.clicked.connect(lambda: remove_from_layout(timer, layout, widget))

        layout.addWidget(label_description, 0, 0)
        layout.addWidget(label_time, 1, 0)
        layout.addWidget(btn_remove, 2, 0)

        self.timers_layout.addWidget(widget)

    def add_timer(self) -> None:
        new_timer = NewTimerDialog()
        if new_timer.exec():
            description = new_timer.description.text()
            if not description:
                description = "New alarm"
            hour = new_timer.time.time().hour()
            minutes = new_timer.time.time().minute()

            now = datetime.now()
            next_alarm = datetime.fromisoformat(f"{now.year}-{now.month:02}-{now.day:02} {hour:02}:{minutes:02}:00.000")

            alarm_id = Database().add_alarm(description=description, next_alarm=next_alarm)

            self.display_timer(Alarm(id=alarm_id, description=description, next_alarm=next_alarm))

    def remove_timer(self, timer) -> None:
        Database().remove_alarm(key=timer.id)
        self.update_timers()
