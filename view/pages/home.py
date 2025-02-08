from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex, QUrl
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMenu
from PySide6.QtGui import QAction, QClipboard, QDesktopServices
import hashlib

from model import FileScanResultModel, UrlScanResultModel, MostDetectedThreatModel
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileScanResultContainer, UrlScanResultContainer
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
        self.ui.tbl_latestFileScanResults.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tbl_latestFileScanResults.customContextMenuRequested.connect(self.fileScanResultsContextMenu)
        self.ui.tbl_latestUrlScanResults.setModel(self.urlScanResultModel)
        self.ui.tbl_latestUrlScanResults.setColumnWidth(0, 200)
        self.ui.tbl_latestUrlScanResults.doubleClicked.connect(self.urlScanResultsItemClick)
        self.ui.tbl_latestUrlScanResults.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tbl_latestUrlScanResults.customContextMenuRequested.connect(self.urlScanResultsContextMenu)
        self.ui.tbl_topThreatsDetections.setModel(self.mostDetectedThreatModel)
        self.ui.tbl_topThreatsDetections.setColumnWidth(0, 250)

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
        self.signals['openRightBox'].emit(scanResult.file.filename, FileScanResultContainer, {'scanResult': scanResult})

    def urlScanResultsItemClick(self, index: QModelIndex):
        row = index.row()
        scanResult = self.urlScanResultModel.results[row]
        self.signals['openRightBox'].emit('URL Scan Result', UrlScanResultContainer, {'scanResult': scanResult})

    def fileScanResultsContextMenu(self, position):
        menu = QMenu(self.ui.tbl_latestFileScanResults)
        def openFileOrDir(field):
            def _openFileOrDir():
                index = self.ui.tbl_latestFileScanResults.currentIndex()
                row = index.row()
                path = self.fileScanResultModel.results[row].file.get(field)
                QDesktopServices.openUrl(QUrl.fromUserInput(path))
            return _openFileOrDir
        for (label, trigger) in [("Open with default program", openFileOrDir('filepath')),
                                 ("View in directory", openFileOrDir('path')),
                                 ("View in VirusTotal", self.viewFileVirusTotal)]:
            menu.addAction(label).triggered.connect(trigger)
        menu.exec(self.ui.tbl_latestFileScanResults.mapToGlobal(position))

    def viewFileVirusTotal(self, position):
        index = self.ui.tbl_latestFileScanResults.currentIndex()
        row = index.row()
        sha256 = self.fileScanResultModel.results[row].file.sha256
        QDesktopServices.openUrl(f'https://www.virustotal.com/gui/file/{sha256}')

    def urlScanResultsContextMenu(self, position):
        menu = QMenu(self.ui.tbl_latestUrlScanResults)
        for (label, trigger) in [("Copy URL", self.copyURL),
                                 ("Open in Browser", self.openURL),
                                 ("View in VirusTotal", self.viewURLVirusTotal)]:
            menu.addAction(label).triggered.connect(trigger)
        menu.exec(self.ui.tbl_latestUrlScanResults.mapToGlobal(position))

    def copyURL(self, position):
        index = self.ui.tbl_latestUrlScanResults.currentIndex()
        row = index.row()
        url = self.urlScanResultModel.results[row].url.url
        clipboard = QClipboard()
        clipboard.clear()
        clipboard.setText(url)

    def openURL(self, position):
        index = self.ui.tbl_latestUrlScanResults.currentIndex()
        row = index.row()
        url = self.urlScanResultModel.results[row].url.url
        QDesktopServices.openUrl(url)

    def viewURLVirusTotal(self, position):
        index = self.ui.tbl_latestUrlScanResults.currentIndex()
        row = index.row()
        url = self.urlScanResultModel.results[row].url.url
        sha256 = hashlib.sha256(url.encode('utf-8')).hexdigest()
        QDesktopServices.openUrl(f'https://www.virustotal.com/gui/url/{sha256}')

    def updateSummary(self):
        filesScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM file_scan_result')
        self.ui.label_statsFilesScanned.setText(f'{filesScanned:,}')
        urlsScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM url_scan_result')
        self.ui.label_statsUrlsScanned.setText(f'{urlsScanned:,}')
        threatsDetected = self.db.fetchOneCol('SELECT COUNT(virus_id) FROM analysis WHERE virus_id IS NOT NULL')
        self.ui.label_statsAnalysisDetections.setText(f'{threatsDetected:,}')
