from PySide6.QtCore import QObject

class Base(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.uiDefinitions()
        self.connectSlotsAndSignals()

    def uiDefinitions(self):
        pass

    def connectSlotsAndSignals(self):
        pass
