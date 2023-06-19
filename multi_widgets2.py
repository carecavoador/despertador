# https://stackoverflow.com/questions/20719030/add-widgets-on-the-fly-in-pyside

import sys

from PySide6 import QtWidgets


class example2(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self.widget)

        # Cria os alarmes e mostra na gui
        self.alarmes = [self.cria_alarme(a) for a in range(3)]
        for i, alarme in enumerate(self.alarmes):
            self.layout.addWidget(alarme, i, 0)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        grid.addWidget(self.scroll, 3, 0)
        self.setLayout(grid)

    @staticmethod
    def remove_widget(layout: QtWidgets.QLayout, widget: QtWidgets.QWidget) -> None:
        """Remove um QWidget do layout e depois da memória."""
        layout.removeWidget(widget)
        widget.deleteLater()

    def cria_alarme(self, i: int) -> QtWidgets.QWidget:
        """Cria um widget de alarme."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)

        label = QtWidgets.QLabel(text=f"Alarme número {i+1}")
        hora = QtWidgets.QTimeEdit()
        botao = QtWidgets.QPushButton(text="Remover")
        botao.clicked.connect(lambda: self.remove_widget(self.layout, widget))

        layout.addWidget(label, 0, 0)
        layout.addWidget(hora, 1, 0)
        layout.addWidget(botao, 2, 0)

        return widget


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    dialog = example2()
    dialog.show()

    sys.exit(app.exec())
