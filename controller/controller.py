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

    def _connectButtons(self):
        self._view.ui.toggleButton.clicked.connect(self._view.toggleMenu)
        self._view.ui.toggleLeftBox.clicked.connect(self._view.toggleLeftBox)
        self._view.ui.extraCloseColumnBtn.clicked.connect(self._view.toggleLeftBox)
        self._view.ui.settingsTopBtn.clicked.connect(self._view.toggleRightBox)

    def _connectNavLinks(self):
        for idx, button in enumerate(self._view.ui.topMenu.findChildren(QPushButton)):
            button.clicked.connect(partial(self._view.changePage, button))
            if idx == 0:
                self._view.changePage(button)
