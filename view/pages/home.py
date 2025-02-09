from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex, QUrl
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMenu, QRadioButton
from PySide6.QtGui import QAction, QClipboard, QDesktopServices
import hashlib

from model import (FileScanResultModel, UrlScanResultModel,
                   TopThreatDetectionModel, TopThreatModel, TopThreatCategoryModel)
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileScanResultContainer, UrlScanResultContainer
from core import DB
from .base import Base

class Home(Base):
    filter = {
        'scanResultType': None,
        'threatsViewBy': None
    }

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.fileScanResultModel = FileScanResultModel(self.db)
        self.urlScanResultModel = UrlScanResultModel(self.db)
        self.topThreatDetectionModel = TopThreatDetectionModel(self.db)
        self.topThreatModel = TopThreatModel(self.db)
        self.topThreatCategoryModel = TopThreatCategoryModel(self.db)
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
        self.ui.tbl_topThreatsDetections.setModel(self.topThreatDetectionModel)
        self.ui.tbl_topThreatsDetections.setColumnWidth(0, 250)
        self.ui.tbl_topThreats.setModel(self.topThreatModel)
        self.ui.tbl_topThreats.setColumnWidth(0, 200)
        self.ui.tbl_topThreatsCategories.setModel(self.topThreatCategoryModel)

    def connectSlotsAndSignals(self):
        self.signals['pageChanged'].connect(self.pageChanged)
        buttonGroupMapping = {
            'radioButton_filterByAll': 'all',
            'radioButton_filterByFile': 'file',
            'radioButton_filterByURL': 'url',
            'radioButton_viewByThreats': 'threats',
            'radioButton_viewByCategories': 'categories',
        }
        def buttonGroupToggled(filterName):
            def toggled(btn: QRadioButton):
                if btn.isChecked():
                    self.filter[filterName] = buttonGroupMapping[btn.objectName()]
                    if filterName == 'scanResultType':
                        self.topThreatDetectionModel.loadData(self.filter[filterName])
                    else:
                        idx = 0 if self.filter[filterName] == 'threats' else 1
                        self.ui.stackedWidget_topThreats.setCurrentIndex(idx)
            return toggled
        for (filterName, buttonGroup) in [('scanResultType', self.ui.buttonGroup_homeFilterBy),
                                          ('threatsViewBy', self.ui.buttonGroup_homeViewBy)]:
            buttonGroup.buttonToggled.connect(buttonGroupToggled(filterName))

    def loadData(self):
        self.fileScanResultModel.loadData()
        self.urlScanResultModel.loadData()
        self.topThreatDetectionModel.loadData(self.filter['scanResultType'])
        self.topThreatModel.loadData()
        self.topThreatCategoryModel.loadData()
        self.updateSummary()

    def pageChanged(self, idx):
        if idx == 0:
            self.loadData()

    def setFilter(self, filterBy):
        self.filterBy = filterBy
        self.topThreatDetectionModel.loadData(self.filterBy)

    def fileScanResultsItemClick(self, index: QModelIndex):
        row = index.row()
        scanResult = self.fileScanResultModel.results[row]
        scanResult.file = File(scanResult.file | self.fileScanResultModel.fetchFileInfo(scanResult.file.id))
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
        threatsDetected = self.db.fetchOneCol('SELECT COUNT(id) FROM threat')
        self.ui.label_statsThreatsDetected.setText(f'{threatsDetected:,}')
        analysisDetections = self.db.fetchOneCol('SELECT COUNT(virus_id) FROM analysis WHERE virus_id IS NOT NULL')
        self.ui.label_statsAnalysisDetections.setText(f'{analysisDetections:,}')
