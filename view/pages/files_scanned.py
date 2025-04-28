from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QModelIndex

from model import FileModel, FileScanResultModel, FileTypeModel
from lib.entity import File
from view.ui.ui_main import Ui_MainWindow
from core import DB, Router, Route
from .base import Base
from view.utils import createContextMenu
from widgets import FileScanResultContainer

class FilesScanned(Base):
    filter = {
        'file_type': None,
        'search': None
    }

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.router: Router = ctx.get('router')
        self.fileModel = FileModel(self.db, show_extra_cols=True)
        self.fileScanResultModel = FileScanResultModel(self.db)
        self.fileTypeModel = FileTypeModel(self.db)
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_filesScanned.setModel(self.fileModel)
        self.ui.tbl_filesScanned.doubleClicked.connect(self.filesItemClick)
        self.ui.tbl_fileScanResults.setModel(self.fileScanResultModel)
        self.ui.tbl_fileScanResults.doubleClicked.connect(self.fileScanResultsItemClick)

    def connectSlotsAndSignals(self):
        self.router.routeUpdated.connect(self.routeUpdated)
        self.fileTypeModel.loaded.connect(self.fileTypesLoaded)
        self.ui.comboBox_fileTypeFilter.currentIndexChanged.connect(
            lambda idx: self.setFilter(file_type=self.fileTypeModel.fileTypes[idx-1] if idx > 0 else -1).loadData(loadFileTypes=False)
            if not self._filterReset else None
        )
        self.ui.btn_back_2.clicked.connect(lambda: self.router.back())
        self.ui.lineEdit_fileNameSearch.textChanged.connect(
            lambda x: self.setFilter(search=x).loadData(loadFileTypes=False)
            if not self._filterReset else None
        )

    def routeUpdated(self, route: Route):
        if route.route == Route.ROUTE_FILES_SCANNED:
            self._filterReset = True
            self.ui.lineEdit_fileNameSearch.clear()
            self.ui.tbl_fileScanResults.setVisible(False)
            searchFilter = route.params or {}
            self.setFilter(reset=True, **searchFilter)
            if 'search' in searchFilter:
                self.ui.lineEdit_fileNameSearch.setText(searchFilter['search'])
            self.loadData()

    def fileTypesLoaded(self, data):
        self.ui.comboBox_fileTypeFilter.clear()
        items = ['- Any -'] + [fileType['description'] for fileType in data]
        self.ui.comboBox_fileTypeFilter.addItems(items)
        self._filterReset = False
        if self.filter['file_type'] is not None:
            self.ui.comboBox_fileTypeFilter.setCurrentIndex(items.index(self.filter['file_type']['name']))

    def loadData(self, loadFiles=True, loadFileTypes=True):
        if loadFiles:
            self.fileModel.loadData(search=self.filter)
        if loadFileTypes:
            self.fileTypeModel.loadData()

    def setFilter(self, file_type=None, search=None, reset=False):
        if reset or file_type is not None:
            self.filter['file_type'] = file_type if file_type != -1 else None
        if reset or search is not None:
            self.filter['search'] = search
        return self

    def filesItemClick(self, index: QModelIndex):
        row = index.row()
        data = self.fileModel._data[row]
        self.fileScanResultModel.loadData(search={'file': data['file'].id})
        self.ui.tbl_fileScanResults.setVisible(True)

    def fileScanResultsItemClick(self, index: QModelIndex):
        row = index.row()
        scanResult = self.fileScanResultModel.results[row]
        scanResult.file = File(scanResult.file | self.fileScanResultModel.fetchFileInfo(scanResult.file.id))
        self.signals['openRightBox'].emit(scanResult.file.filename, FileScanResultContainer, {'scanResult': scanResult})
