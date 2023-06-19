import sys
from PySide6 import QtWidgets, QtCore

from db import Banco

class NewTimerDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Novo alarme")

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.dialog_buttons = QtWidgets.QDialogButtonBox(buttons)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.label_time = QtWidgets.QLabel("Horário do novo alarme:")
        self.time = QtWidgets.QTimeEdit()
        self.label_desc = QtWidgets.QLabel("Descrição:")
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
        self.db = Banco()
        self.setWindowTitle("Alarmes")
        self.setMinimumSize(240, 360)

        self.painel_principal = QtWidgets.QWidget()
        self.layout_principal = QtWidgets.QGridLayout(self.painel_principal)

        self.btn_add = QtWidgets.QPushButton("Novo alarme")
        self.btn_add.clicked.connect(self.add_timer)

        self.painel_timers = QtWidgets.QWidget()
        self.layout_timers = QtWidgets.QVBoxLayout(self.painel_timers)
        self.layout_timers.addStretch()
        self.layout_timers.setDirection(self.layout_timers.Direction.BottomToTop)

        self.layout_principal.addWidget(self.btn_add, 0, 0)
        self.layout_principal.addWidget(self.painel_timers, 1, 0)

        # DATA
        self.timers = [(t[0], t[1], t[2], t[3]) for t in self.db.alarmes]
        self.display_timers()

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(self.scroll.verticalScrollBarPolicy().ScrollBarAlwaysOn)
        self.scroll.setWidget(self.painel_principal)
        self.setCentralWidget(self.scroll)

    def display_timers(self) -> None:
        def remove_timer(layout: QtWidgets.QLayout, widget: QtWidgets.QWidget, id: int) -> None:
            layout.removeWidget(widget)
            widget.deleteLater()
            self.db.remove_alarme(key=id)
            self.timers.remove((id, widget))

        for timer in self.timers:
            id = timer[0]
            description = timer[1]
            hour = timer[2]
            minutes = timer[3]
            
            widget = QtWidgets.QGroupBox()
            layout = QtWidgets.QGridLayout(widget)

            label = QtWidgets.QLabel(f"<b>{description if description else 'Alarme'}</b>")
            label_time = QtWidgets.QLabel(f"{hour:02}:{minutes:02}")
            btn_remove = QtWidgets.QPushButton(text="Remover alarme")
            btn_remove.clicked.connect(lambda: remove_timer(layout, widget, id))

            layout.addWidget(label, 0, 0)
            layout.addWidget(label_time, 1, 0)
            layout.addWidget(btn_remove, 2, 0)

            self.layout_timers.addWidget(widget)

    def add_timer(self) -> None:
        new_timer = NewTimerDialog()
        if new_timer.exec():
            description = new_timer.description.text()
            hour = new_timer.time.time().hour()
            minutes = new_timer.time.time().minute()
            id = self.db.add_alarme(description, hour, minutes)
            self.timers.append((id, self.display_timer(id=id, description=description, hour=hour, minutes=minutes)))
        self.update_timers()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = TimerWindow()
    dialog.show()
    sys.exit(app.exec())
