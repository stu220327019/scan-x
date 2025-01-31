from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from model import FileScanModel
from ..ui.ui_main import Ui_MainWindow


class FileScan2(QObject):
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.model = FileScanModel()
        self.uiDefinitions()
        self.connect_slots_and_signals()
        self.files = []

    def uiDefinitions(self):
        self.ui.tree_filelist.setModel(self.model)
        self.ui.tree_filelist.setColumnWidth(0, 300)
        self.ui.tree_filelist.setColumnWidth(1, 150)

    def connect_slots_and_signals(self):
        self.ui.btn_fileSelect.clicked.connect(self.fileBrowse)
        self.ui.fileScanDrop.dropSignal.connect(self.filesDropped)

    def fileBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if dlg.exec_():
            selectedFiles = dlg.selectedFiles()
            for filepath in selectedFiles:
                self.model.addFile(filepath)

    def filesDropped(self, filepaths):
        for filepath in filepaths:
            self.model.addFile(filepath)
