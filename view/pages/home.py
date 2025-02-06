from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from model import FileScanResultModel, MostDetectedThreatModel
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer
from core import DB
from .base import Base

class Home(Base):
    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.fileScanResultModel = FileScanResultModel(self.db)
        self.mostDetectedThreatModel = MostDetectedThreatModel(self.db)
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tree_fileScanResults.setModel(self.fileScanResultModel)
        self.ui.tree_fileScanResults.setColumnWidth(1, 150)
        self.ui.tree_fileScanResults.doubleClicked.connect(self.fileScanResultsItemClick)
        self.ui.tree_mostDetectedVirus.setModel(self.mostDetectedThreatModel)
        self.ui.tree_mostDetectedVirus.setColumnWidth(0, 250)

    def connectSlotsAndSignals(self):
        self.signals['pageChanged'].connect(self.pageChanged)

    def loadData(self):
        self.fileScanResultModel.loadData()
        self.mostDetectedThreatModel.loadData()
        self.updateSummary()

    def pageChanged(self, idx):
        if idx == 0:
            self.loadData()

    def fileScanResultsItemClick(self, index: QModelIndex):
        row = index.row()
        scanResult = self.fileScanResultModel.results[row]
        self.signals['openRightBox'].emit(scanResult.file.filename, FileDetailsContainer, {'scanResult': scanResult})

    def updateSummary(self):
        filesScaned = self.db.fetchOneCol('SELECT COUNT(id) FROM file_scan_result')
        self.ui.label_filesScanned.setText(f'{filesScaned:,}')
        threatsDetected = self.db.fetchOneCol('SELECT COUNT(virus_id) FROM analysis WHERE virus_id IS NOT NULL')
        self.ui.label_threatsDetected.setText(f'{threatsDetected:,}')
