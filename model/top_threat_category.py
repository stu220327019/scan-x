from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor, QIcon
import json

from core import DB

class TopThreatCategoryModel(QAbstractTableModel):
    threatCategories = []
    loaded = Signal(list)

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

    def rowCount(self, parent=QModelIndex()):
        return len(self.threatCategories) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Threat', 'Detected'][section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole,):
            return None
        row = index.row()
        col = index.column()
        return self.threatCategories[row][['name', 'detected'][col]]

    def loadData(self, viewBy=None):
        query = """
        SELECT c.id, c.name, COUNT(*) AS detected
        FROM threat t, threat_category c, threats_categories tc
        WHERE tc.threat_id = t.id AND tc.threat_category_id = c.id
        GROUP BY c.id
        ORDER BY detected DESC
        """
        rows = self.db.fetchAll(query)
        self.beginResetModel()
        self.threatCategories.clear()
        for row in rows:
            self.threatCategories.append(row)
        self.endResetModel()
        self.loaded.emit(self.threatCategories)
