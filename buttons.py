from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber
from display import Display
from PySide6.QtCore import Slot


if TYPE_CHECKING:
    from main_window import MainWindow
    from display import Display


# criando a classe de botoes
class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    # configurando estilo do botao
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(50, 75)


# criando uma grid de botoes
class ButtonsGrid(QGridLayout):
    def __init__(
        self, display: Display, info, window: "MainWindow", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ["C", "D", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.display = display
        self.window = window
        self.info = info
        self._equation = ""
        self._equationInitilValue = "Sua conta"
        self._left = None
        self._rigth = None
        self._op = None
        self.equation = self._equationInitilValue
        self._makeGrid()

    @property  # getter
    def equation(self):
        return self._equation

    @equation.setter  # setter que irá mostrar o resultado da conta no display
    def equation(self, value):
        self._equation = value
        self.info.setText(value)


    # criando grid de botoes. Usando um for para adicionar os caracteres aos botoes
    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.imputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)
                # verificando caractres especiais para criar layout diferente dos numeros
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)
                self.addWidget(button, i, j)  # aqui o botao recebe o caractere

                # variavel chamando o metodo que chamar a funcao que adia o slot
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(
        self, button, slot
    ):  # conecta o botao clicado passando para o slot
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):  # configura os botoes especiais
        text = button.text()

        if text == "C":  # verifica se e o botao "C" para limpar o display
            self._connectButtonClicked(button, self._clear)
        if (
            text == "D"
        ):  # verifica se e o botao e o backspace para apagar da direita p\ esquerda
            self._connectButtonClicked(button, self.display.backspace)
        if (
            text == "N"
        ):  # verifica se e o botao e o 
            self._connectButtonClicked(button, self._invertNumber)
        
        if text in "+-/*^":  # verifica se e o botao e um dos operadores
            self._connectButtonClicked(
                button, self._makeSlot(self._configLeftOp, text)
            )

        if text == "=":  # verifica se e o botao e um dos operadores
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):  # funcao que adia o verdadeiro slot
        @Slot(bool)
        def realSlot(_):  # slot verdadeiro
            func(*args, **kwargs)

        return realSlot
    
    # funcao que inverte o número negativo
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return
        number = convertToNumber(displayText) * -1
        self.display.setText(str(number))
        self.display.setFocus()

    # funcao que mostra a informação no display quando o botao é clicado
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = (
            self.display.text() + text
        )  # verifica o o que o botao esta tentando inserir
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)
        self.display.setFocus()


    @Slot()
    def _clear(self):  # metodo para limpar o display
        self.display.clear()
        self._left = None
        self._rigth = None
        self._op = None
        self.equation = self._equationInitilValue
        self.display.clear()
        self.display.setFocus()


    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()


    @Slot()
    def _configLeftOp(self, text):  # aqui o metodo dos operadores e executado ao clicar no botao
        displayText = self.display.text()  # numero da esquerda left
        self.display.clear()  # limpa o display
        self.display.setFocus()
        # checa se o operador foi inserido sem ter outro numero antes
        if not isValidNumber(displayText) and self._left is None:
            self._showError("você não digitou nada. ")
            return
        # se houver numero da esquerda,
        # nao faz nada, aguarda o numero da direita
        if self._left is None:
            self._left = convertToNumber(displayText)
        self._op = text
        self.equation = f"{self._left} {self._op} ??"

    # metodo executado ao clicar no botao '='
    @Slot()
    def _eq(self):
        displayText = self.display.text()  # o que tem no display
        # verifica se o caractere e valido
        if not isValidNumber(displayText) or self._left is None:
            self._showError("Conta incompleta")
            return
        self._rigth = convertToNumber(displayText)  # caso o numero seja valido
        self.equation = f"{self._left} {self._op} {self._rigth}"  # mostra os dois numeros e operador
        result = "error"
        try:
            # condicional para realizar potencia
            if "^" in self.equation:
                result = eval(self.equation.replace("^", "**"))
            else:
                result = eval(self.equation)
        # tratamento caso tente dividir por 0
        except ZeroDivisionError:
            self._showError("Divisão por zero. ")
        except OverflowError:
            self._showError("Número grande para calcular")
        self.display.clear()
        self.info.setText(
            f"{self.equation} = {result}"
        )  # mostra o resultado no display
        # atribui o resultado a variavel da esquerda
        # para continuar a conta
        self._left = result
        # define a variavel da direita como None
        # para continuar a conta
        self._rigth = None
        self.display.setFocus()
        if result == "error":
            self._left = None

    # metodo que mostra a caixa de error ao usuario
    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

