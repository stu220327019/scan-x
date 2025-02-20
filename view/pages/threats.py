from model import TopThreatModel, TopThreatCategoryModel
from view.ui.ui_main import Ui_MainWindow
from core import DB, Router, Route
from .base import Base
from view.utils import createContextMenu

class Threats(Base):
    filter = {
        'category': None
    }

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        self.router: Router = ctx.get('router')
        self.threatModel = TopThreatModel(self.db)
        self.threatCategoryModel = TopThreatCategoryModel(self.db)
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_threats.setModel(self.threatModel)
        self.ui.tbl_threats.setColumnWidth(0, 200)
        contextMenuActions = [
            ('Google Lookup', lambda res: QDesktopServices.openUrl('https://www.google.com/search?&q={}'.format(res['name'])))
        ]
        createContextMenu(self.ui.tbl_threats, self.threatModel, 'threats', contextMenuActions)
        # self.ui.comboBox_threatCategoryFilter.setModel(self.threatCategoryModel)

    def connectSlotsAndSignals(self):
        self.router.routeUpdated.connect(self.routeUpdated)
        self.threatCategoryModel.loaded.connect(self.categoriesLoaded)
        self.ui.comboBox_threatCategoryFilter.currentIndexChanged.connect(
            lambda idx: self.setFilter(category=self.threatCategoryModel.threatCategories[idx-1] if idx > 0 else None).loadData(True))

    def routeUpdated(self, route: Route):
        if route.route == Route.ROUTE_THREATS:
            self.setFilter().loadData()

    def categoriesLoaded(self, data):
        self.ui.comboBox_threatCategoryFilter.clear()
        self.ui.comboBox_threatCategoryFilter.addItems(
            ['- Any -'] + [category['name'] for category in data]
        )

    def loadData(self, threatsOnly=False):
        self.threatModel.loadData(search=self.filter)
        if not threatsOnly:
            self.threatCategoryModel.loadData()

    def setFilter(self, category=None):
        self.filter['category'] = category
        return self
