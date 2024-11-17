from controller import *
from model import *
from view import *
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase,QIcon
import sys


class App():
    def __init__(self) -> None:
        self.model = Model()
        self.view = View(self.model)
        self.controller = Controller(self.view, self.model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # QFontDatabase.addApplicationFont('resources/fonts/segoeui.ttf')
    # app.setWindowIcon(QIcon("icon.ico"))
    App()
    sys.exit(app.exec())
