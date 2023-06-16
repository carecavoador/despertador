import sys
import config
import datetime as dt

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QTimeEdit,
    QLabel
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QTime, QTimer
from janela_alarme import Ui_MainWindow


ALARME_TOCOU = False
SEGUNDO = 1000
MINUTO = 60 * SEGUNDO


class NovaJanela(QMainWindow):
    """Janela principal do programa."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Nova janela")
        layout = QVBoxLayout(self)
        self.alarme = QTimeEdit(time=QTime(4, 20))
        self.texto = QLabel(text="Teste")
        layout.addChildWidget(self.alarme)
        layout.addWidget(self.texto)
        self.setFixedSize(300, 130)


class JanelaPrincipal(QMainWindow, Ui_MainWindow):
    """Janela principal do programa."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(300, 130)
        self.edit_hora.timeChanged.connect(self.atualiza_hora)
        self.hora_salva = config.carrega_config()
        self.edit_hora.setTime(
            QTime(self.hora_salva["hora"], self.hora_salva["minutos"])
        )

    def atualiza_hora(self) -> None:
        global ALARME_TOCOU
        hora = self.edit_hora.time()
        config.salva_config(hora=hora.hour(), minutos=hora.minute())
        ALARME_TOCOU = False


def verifica_alarme() -> None:
    global ALARME_TOCOU
    alarme = config.carrega_config()
    agora = dt.datetime.now()
    if (
        alarme["hora"] == agora.hour
        and alarme["minutos"] == agora.minute
        and not ALARME_TOCOU
    ):
        print("Soa o alarme")
        aviso = QMessageBox()
        aviso.setWindowTitle("Alarme")
        aviso.setText("Hora de tomar o remédio!")
        aviso.exec()
        ALARME_TOCOU = True


def main() -> None:
    """Início do programa"""

    app = QApplication(sys.argv)

    # Não encerrar ao fechar a janela
    # app.setQuitOnLastWindowClosed(False)

    # Timer
    timer = QTimer()
    timer.start(MINUTO)
    timer.timeout.connect(verifica_alarme)

    # janela = JanelaPrincipal()
    janela = NovaJanela()

    # Coloca o icone na bandeja
    tray = QSystemTrayIcon()
    icon = QIcon("relogio-de-mesa.png")
    tray.setIcon(icon)
    tray.setVisible(True)

    # Cria o menu da bandeja
    menu = QMenu()
    abrir = QAction("Horário do despertador")
    abrir.triggered.connect(janela.show)
    menu.addAction(abrir)

    sair = QAction("Fechar")
    sair.triggered.connect(app.quit)
    menu.addAction(sair)

    # Adiciona o menu à bandeja
    tray.setContextMenu(menu)

    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
