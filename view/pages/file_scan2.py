from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from model import FileScanModel
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer


class FileScan2(QObject):
    model = FileScanModel()
    files = []

    def __init__(self, ui: Ui_MainWindow, signals=None):
        super().__init__()
        self.ui = ui
        self.signals = signals

        self.uiDefinitions()
        self.connect_slots_and_signals()

    def uiDefinitions(self):
        self.ui.tree_filelist.setModel(self.model)
        self.ui.tree_filelist.setColumnWidth(0, 300)
        self.ui.tree_filelist.setColumnWidth(1, 150)

    def connect_slots_and_signals(self):
        self.ui.btn_fileSelect.clicked.connect(self.fileBrowse)
        self.ui.fileScanDrop.dropSignal.connect(self.filesDropped)
        self.ui.tree_filelist.doubleClicked.connect(self.filelistItemClick)
        self.ui.tree_filelist.keyPressed.connect(self.filelistkeyPressed)

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

    def filelistkeyPressed(self, event):
        if event.key() == Qt.Key_Delete:
            selected = self.ui.tree_filelist.currentIndex()
            if selected.isValid():
                self.model.removeFile(selected)

    def filelistItemClick(self, index: QModelIndex):
        row = index.row()
        fileInfo = self.model.files[row]
        self.signals['openRightBox'].emit(fileInfo.get('filename'), FileDetailsContainer, {'fileInfo': fileInfo})
