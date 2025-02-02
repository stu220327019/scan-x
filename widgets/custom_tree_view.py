from PySide6.QtWidgets import QTreeView
from PySide6.QtCore import Signal

class CustomTreeView(QTreeView):
    keyPressed = Signal(object)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.keyPressed.emit(event)
