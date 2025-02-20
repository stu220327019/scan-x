from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex, QUrl
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QMenu, QRadioButton
from PySide6.QtGui import QAction, QClipboard, QDesktopServices
import hashlib
import pygal

from model import (FileScanResultModel, UrlScanResultModel,
                   TopThreatDetectionModel, TopThreatModel, TopThreatCategoryModel)
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileScanResultContainer, UrlScanResultContainer
from core import DB, Route, Router
from .base import Base
from view.utils import createContextMenu

class Home(Base):
    filter = {
        'scanResultType': None,
        'threatsViewBy': None
    }

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.router: Router = ctx.get('router')
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
        def openFileOrDir(field):
            def _openFileOrDir(res):
                path = res.file.get(field)
                QDesktopServices.openUrl(QUrl.fromUserInput(path))
            return _openFileOrDir
        def delFileScanResult(res):
            self.fileScanResultModel.delScanResult(res.id)
            self.loadData()
        latestFileScanResultsContextMenuActions = [
            ("Open with default program", openFileOrDir('filepath')),
            ("View in directory", openFileOrDir('path')),
            ("View in VirusTotal", lambda res:\
             QDesktopServices.openUrl(f'https://www.virustotal.com/gui/file/{res.file.sha256}')),
            ("Delete", delFileScanResult)]
        createContextMenu(self.ui.tbl_latestFileScanResults, self.fileScanResultModel, 'results', latestFileScanResultsContextMenuActions)
        self.ui.tbl_latestUrlScanResults.setModel(self.urlScanResultModel)
        self.ui.tbl_latestUrlScanResults.setColumnWidth(0, 200)
        self.ui.tbl_latestUrlScanResults.doubleClicked.connect(self.urlScanResultsItemClick)
        def copyURL(res):
            clipboard = QClipboard()
            clipboard.clear()
            clipboard.setText(res.url.url)
        def viewURLVirusTotal(res):
            url = res.url.url
            sha256 = hashlib.sha256(url.encode('utf-8')).hexdigest()
            QDesktopServices.openUrl(f'https://www.virustotal.com/gui/url/{sha256}')
        def delURLScanResult(res):
            self.urlScanResultModel.delScanResult(res.id)
            self.loadData()
        latestUrlScanResultsContextMenuActions = [
            ("Copy URL", copyURL),
            ("Open in Browser", lambda res: QDesktopServices.openUrl(res.url.url)),
            ("View in VirusTotal", viewURLVirusTotal),
            ("Delete", delURLScanResult)
        ]
        createContextMenu(self.ui.tbl_latestUrlScanResults, self.urlScanResultModel, 'results', latestUrlScanResultsContextMenuActions)
        self.ui.tbl_topThreatsDetections.setModel(self.topThreatDetectionModel)
        self.ui.tbl_topThreatsDetections.setColumnWidth(0, 250)
        topThreatsDetectionContextMenuActions = [
            ('Google Lookup', lambda res: QDesktopServices.openUrl('https://www.google.com/search?&q={}'.format(res['name'])))
        ]
        createContextMenu(self.ui.tbl_topThreatsDetections, self.topThreatDetectionModel, 'threats', topThreatsDetectionContextMenuActions)
        self.ui.tbl_topThreats.setModel(self.topThreatModel)
        self.ui.tbl_topThreats.setColumnWidth(0, 200)
        topThreatsContextMenuActions = [
            ('Google Lookup', lambda res: QDesktopServices.openUrl('https://www.google.com/search?&q={}'.format(res['name'])))
        ]
        createContextMenu(self.ui.tbl_topThreats, self.topThreatModel, 'threats', topThreatsContextMenuActions)
        self.ui.tbl_topThreatsCategories.setModel(self.topThreatCategoryModel)

    def connectSlotsAndSignals(self):
        self.router.routeUpdated.connect(self.routeUpdated)
        self.topThreatCategoryModel.loaded.connect(self.topThreatCategoriesloaded)
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

    def routeUpdated(self, route: Route):
        if route.route == Route.ROUTE_HOME:
            self.loadData()

    def topThreatCategoriesloaded(self, data):
        style = pygal.style.Style(tooltip_font_size=50)
        pie_chart = pygal.Pie(human_readable=True, fill=True, show_legend=False, style=style, inner_radius=.4)
        for cat in data:
            pie_chart.add(cat['name'], cat['detected'])
        data_uri = pie_chart.render_data_uri()
        self.ui.webEngineView_topThreatsCategories.load(QUrl(data_uri))

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

    def updateSummary(self):
        filesScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM file_scan_result')
        self.ui.label_statsFilesScanned.setText(f'{filesScanned:,}')
        urlsScanned = self.db.fetchOneCol('SELECT COUNT(id) FROM url_scan_result')
        self.ui.label_statsUrlsScanned.setText(f'{urlsScanned:,}')
        threatsDetected = self.db.fetchOneCol('SELECT COUNT(id) FROM threat')
        self.ui.label_statsThreatsDetected.setText(f'{threatsDetected:,}')
        analysisDetections = self.db.fetchOneCol('SELECT COUNT(virus_id) FROM analysis WHERE virus_id IS NOT NULL')
        self.ui.label_statsAnalysisDetections.setText(f'{analysisDetections:,}')
