from controller import *
from model import *
from view import *
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase,QIcon
import sys
import asyncio
import os
from qasync import QEventLoop

def main():
    # os.putenv('QT_QPA_PLATFORM','windows:darkmode=0')
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    model = Model()
    view = View(model)
    controller = Controller(view, model)

    view.show()

    # sys.exit(app.exec())
    with loop:
        loop.run_forever()


if __name__ == '__main__':
    main()
