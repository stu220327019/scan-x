from PySide6.QtWidgets import *
from PySide6.QtCore import Signal

class FileDropWidget(QWidget):
    dropSignal = Signal(list)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    # def __init__(self, parent):
    #     super().__init__()
        # self.parent = parent
        # self.setParent(parent)
    #     self.setStyleSheet("""
	# border: 2px dashed rgb(220, 220, 220);
	# border-radius: 5px;
    #     """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.dropSignal.emit(files)
