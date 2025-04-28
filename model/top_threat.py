from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from operator import itemgetter

from core import DB, QueryBuilder

class TopThreatModel(QAbstractTableModel):
    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db
        self.threats = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.threats) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Threat', 'Detected', 'Categories', 'Detected (Unique)'][section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole,):
            return None
        row = index.row()
        col = index.column()
        val = self.threats[row][['name', 'detected', 'categories'][col]]
        return str.join(', ', val) if type(val) == list else val

    def loadData(self, viewBy=None, search=None):
        query = QueryBuilder()

        subquery = QueryBuilder()\
                   .SELECT('t.id', 't.name', ('detected', 'COUNT(*)'))\
                   .FROM(('t', 'threat'), ('f', 'file'))\
                   .WHERE('f.threat_id = t.id')\
                   .GROUP_BY('t.id')\
                   .ORDER_BY('detected DESC')\
                   .LIMIT('100')

        if search:
            if search['category']:
                subquery.WHERE('tc.threat_category_id = ?')
                query.add_param(search['category']['id'])
                subquery.JOIN('threats_categories tc ON tc.threat_id = t.id')
            if search['threatName']:
                subquery.WHERE('t.name LIKE ?')
                query.add_param(f'%{search['threatName']}%')

        query\
            .SELECT('t.*', ('categories', 'JSON_GROUP_ARRAY(c.name)'))\
            .FROM('t', ('c', 'threat_category'), ('tc', 'threats_categories'))\
            .WHERE('tc.threat_id = t.id')\
            .WHERE('tc.threat_category_id = c.id')\
            .GROUP_BY('t.id')\
            .ORDER_BY('detected DESC')\
            .WITH(('t', str(subquery)))

        rows = self.db.fetchAll(str(query), query.params())
        self.beginResetModel()
        self.threats.clear()
        for row in rows:
            row['categories'] = json.loads(row['categories'])
            self.threats.append(row)
        self.endResetModel()
