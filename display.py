from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variables import BIG_FONT_SIZE, MINIMUM_WIDTH, TEXT_MARGIN
from utils import isEmpty, isNumOrDot

#criando a classe de display que herda de QLINEDIT
class Display(QLineEdit):
    #comandos para emitir o signal
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    imputPressed = Signal(str)
    operatorPressed= Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    #configurando o estilo do display
    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)] #define as margens do display altura, largura etc.
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;') #define a fonte de saida
        self.setMinimumHeight(BIG_FONT_SIZE * 3) # tamanho da janela do display
        self.setMinimumWidth(MINIMUM_WIDTH) # define a largura da calculadora
        self.setAlignment(Qt.AlignmentFlag.AlignRight) #definindo o alinhamento
        self.setTextMargins(*margins) # extrai as variaveis da margens

    #funcao que recebe o que esta digitando
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        #verifica se a tecla é enter ou return
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsc = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
        if isEnter or text == '=':
            #ao pressionar o enter ou return o signal é enviado para a makegrid
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete:
            #ao pressionar o enter ou return o signal é enviado para a makegrid
            self.delPressed.emit()
            return event.ignore()
        if isEsc:
            #ao pressionar o enter ou return o signal é enviado para a makegrid
            self.clearPressed.emit()
            return event.ignore()
        
        if isOperator:
            #ao pressionar o enter ou return o signal é enviado para a makegrid
            if text.lower() == 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
        
        #metodo para nao deixar passar sem texto
        if isEmpty(text):
            return event.ignore()
        #metodo imput p/ capturar numeros do teclado
        if isNumOrDot(text):
            self.imputPressed.emit(text)
            return event.ignore()