from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel

class LinkLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
