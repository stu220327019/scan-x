from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from model import FileScanResultModel, UrlScanResultModel, MostDetectedThreatModel
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer
from core import DB
from .base import Base

class Home(Base):
    filtered = Signal(str)
    filterBy = 'all'

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.fileScanResultModel = FileScanResultModel(self.db)
        self.urlScanResultModel = UrlScanResultModel(self.db)
        self.mostDetectedThreatModel = MostDetectedThreatModel(self.db)
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_latestFileScanResults.setModel(self.fileScanResultModel)
        self.ui.tbl_latestFileScanResults.setColumnWidth(1, 150)
        self.ui.tbl_latestFileScanResults.doubleClicked.connect(self.fileScanResultsItemClick)
        self.ui.tbl_latestUrlScanResults.setModel(self.urlScanResultModel)
        self.ui.tbl_latestUrlScanResults.setColumnWidth(0, 200)
        self.ui.tbl_mostDetectedVirus.setModel(self.mostDetectedThreatModel)
        self.ui.tbl_mostDetectedVirus.setColumnWidth(0, 250)

    def connectSlotsAndSignals(self):
        self.signals['pageChanged'].connect(self.pageChanged)
        self.filtered.connect(self.setFilter)
        for (x, radioBtn) in [('all', self.ui.op_TopThreatsfilterAll),
                              ('file', self.ui.op_TopThreatsfilterFiles),
                              ('url', self.ui.op_TopThreatsfilterURLs)]:
            def toggled(x):
                def f(checked):
                    if checked:
                        self.filtered.emit(x)
                return f
            radioBtn.toggled.connect(toggled(x))

    def loadData(self):
        self.fileScanResultModel.loadData()
        self.urlScanResultModel.loadData()
        self.mostDetectedThreatModel.loadData(self.filterBy)
        self.updateSummary()

    def pageChanged(self, idx):
        if idx == 0:
            self.loadData()

    def setFilter(self, filterBy):
        self.filterBy = filterBy
        self.mostDetectedThreatModel.loadData(self.filterBy)

    def fileScanResultsItemClick(self, index: QModelIndex):
        row = index.row()
        scanResult = self.fileScanResultModel.results[row]
        self.signals['openRightBox'].emit(scanResult.file.filename, FileDetailsContainer, {'scanResult': scanResult})

    def updateSummary(self):
        filesScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM file_scan_result')
        self.ui.label_statsFilesScanned.setText(f'{filesScanned:,}')
        urlsScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM url_scan_result')
        self.ui.label_statsUrlsScanned.setText(f'{urlsScanned:,}')
        threatsDetected = self.db.fetchOneCol('SELECT COUNT(virus_id) FROM analysis WHERE virus_id IS NOT NULL')
        self.ui.label_statsThreatsDetected.setText(f'{threatsDetected:,}')
