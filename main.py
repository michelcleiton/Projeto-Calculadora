import sys

from info import Info
from display import Display
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH
from styles import setupTheme
from buttons import Button, ButtonsGrid

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #info
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)
    
    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid de botoes
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)


    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()