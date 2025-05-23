from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QModelIndex

from model import TopThreatModel, TopThreatCategoryModel, FileModel
from view.ui.ui_main import Ui_MainWindow
from core import DB, Router, Route
from .base import Base
from view.utils import createContextMenu

class Threats(Base):
    filter = {
        'category': None,
        'threatName': None
    }

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.router: Router = ctx.get('router')
        self.threatModel = TopThreatModel(self.db)
        self.threatCategoryModel = TopThreatCategoryModel(self.db)
        self.fileModel = FileModel(self.db)
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_threats.setModel(self.threatModel)
        self.ui.tbl_threats.setColumnWidth(0, 200)
        contextMenuActions = [
            ('Google Lookup', lambda res: QDesktopServices.openUrl('https://www.google.com/search?&q={}'.format(res['name'])))
        ]
        createContextMenu(self.ui.tbl_threats, self.threatModel, 'threats', contextMenuActions)
        self.ui.tbl_threats.doubleClicked.connect(self.threatsItemClick)
        self.ui.tbl_threatFiles.setModel(self.fileModel)
        # self.ui.comboBox_threatCategoryFilter.setModel(self.threatCategoryModel)

    def connectSlotsAndSignals(self):
        self.router.routeUpdated.connect(self.routeUpdated)
        self.threatCategoryModel.loaded.connect(self.categoriesLoaded)
        self.ui.comboBox_threatCategoryFilter.currentIndexChanged.connect(
            lambda idx: self.setFilter(category=self.threatCategoryModel.threatCategories[idx-1] if idx > 0 else -1).loadData(loadCategories=False)
            if not self._filterReset else None
        )
        self.ui.btn_back.clicked.connect(lambda: self.router.back())
        self.ui.lineEdit_threatNameSearch.textChanged.connect(
            lambda x: self.setFilter(threatName=x).loadData(loadCategories=False)
            if not self._filterReset else None
        )

    def routeUpdated(self, route: Route):
        if route.route == Route.ROUTE_THREATS:
            self._filterReset = True
            self.ui.lineEdit_threatNameSearch.clear()
            self.ui.tbl_threatFiles.setVisible(False)
            searchFilter = route.params or {}
            self.setFilter(reset=True, **searchFilter)
            self.loadData(loadThreats=not searchFilter)

    def categoriesLoaded(self, data):
        self.ui.comboBox_threatCategoryFilter.clear()
        items = ['- Any -'] + [category['name'] for category in data]
        self.ui.comboBox_threatCategoryFilter.addItems(items)
        self._filterReset = False
        if self.filter['category'] is not None:
            self.ui.comboBox_threatCategoryFilter.setCurrentIndex(items.index(self.filter['category']['name']))

    def loadData(self, loadThreats=True, loadCategories=True):
        if loadThreats:
            self.threatModel.loadData(search=self.filter)
        if loadCategories:
            self.threatCategoryModel.loadData()

    def setFilter(self, category=None, threatName=None, reset=False):
        if reset or category is not None:
            self.filter['category'] = category if category != -1 else None
        if reset or threatName is not None:
            self.filter['threatName'] = threatName
        return self

    def threatsItemClick(self, index: QModelIndex):
        row = index.row()
        threat = self.threatModel.threats[row]
        self.fileModel.loadData(search={'threat': threat['id']})
        self.ui.tbl_threatFiles.setVisible(True)
