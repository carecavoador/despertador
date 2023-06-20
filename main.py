import sys
import datetime as dt

# from plyer import notification
from PySide6 import QtWidgets, QtGui, QtCore

from db import Banco
from alarme import Alarme
from janela_nova import TimerWindow


def verifica_alarme() -> None:
    agora = dt.datetime.now()
    alarmes = [[False, Alarme(t[0], t[1], t[2], t[3])] for t in Banco().alarmes]
    for alarme in alarmes:
        hora = alarme[1].hour
        minutos = alarme[1].minutes
        descricao = alarme[1].description
        if (
            hora == agora.hour
            and minutos == agora.minute
        ):
            # notification.notify(
            #     title=f"Alarme {hora:02}:{minutos:02}",
            #     message=descricao,
            #     app_icon="icone.ico",
            #     # timeout=60000
            # )
            aviso = QtWidgets.QMessageBox()
            aviso.setIcon(QtWidgets.QMessageBox.Icon.Information)
            aviso.setWindowTitle(f"Alarme {hora:02}:{minutos:02}")
            aviso.setText(descricao)
            aviso.exec()


def main() -> None:
    """Início do programa"""

    app = QtWidgets.QApplication(sys.argv)

    # Não encerrar ao fechar a janela
    app.setQuitOnLastWindowClosed(False)

    # Timer
    timer = QtCore.QTimer()
    timer.start(1000 * 31)
    timer.timeout.connect(verifica_alarme)

    # janela = JanelaPrincipal()
    janela = TimerWindow()

    # Coloca o icone na bandeja
    tray = QtWidgets.QSystemTrayIcon()
    icon = QtGui.QIcon("icone.ico")
    tray.setIcon(icon)
    tray.setVisible(True)

    # Cria o menu da bandeja
    menu = QtWidgets.QMenu()
    abrir = QtGui.QAction("Verificar alarmes")
    abrir.triggered.connect(janela.show)
    menu.addAction(abrir)

    sair = QtGui.QAction("Fechar")
    sair.triggered.connect(app.quit)
    menu.addAction(sair)

    # Adiciona o menu à bandeja
    tray.setContextMenu(menu)

    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
