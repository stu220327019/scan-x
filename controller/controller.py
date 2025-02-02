from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton
from view import View

class Controller:
    def __init__(self, view, model) -> None:
        self._view: View = view
        self._model = model

        self._connectButtons()
        self._connectNavLinks()
        self.connect_slots_and_signals()

    def _connectButtons(self):
        self._view.ui.toggleButton.clicked.connect(self._view.toggleMenu)
        self._view.ui.toggleLeftBox.clicked.connect(self._view.toggleLeftBox)
        self._view.ui.extraCloseColumnBtn.clicked.connect(self._view.toggleLeftBox)
        # self._view.ui.settingsTopBtn.clicked.connect(self._view.toggleRightBox)
        self._view.ui.settingsTopBtn.clicked.connect(lambda: self._view.toggleRightBoxSignal.emit())
        self._view.ui.btn_extraRightBoxClose.clicked.connect(lambda: self._view.closeRightBoxSignal.emit())
        self._view.ui.extraRightBoxBackdrop.mousePressEvent = lambda x: self._view.closeRightBoxSignal.emit()

    def connect_slots_and_signals(self):
        self._view.toggleRightBoxSignal.connect(self._view.toggleRightBox)
        self._view.openRightBoxSignal.connect(self._view.openRightBox)
        self._view.closeRightBoxSignal.connect(self._view.closeRightBox)

    def _connectNavLinks(self):
        for idx, button in enumerate(self._view.ui.topMenu.findChildren(QPushButton)):
            button.clicked.connect(partial(self._view.changePage, button))
            if idx == 0:
                self._view.changePage(button)
