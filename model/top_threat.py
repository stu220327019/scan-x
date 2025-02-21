from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from operator import itemgetter

from core import DB, QueryBuilder

class TopThreatModel(QAbstractTableModel):
    threats = []

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

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
        qb = QueryBuilder()
        if search:
            if search['category']:
                qb.where('tc.threat_category_id', search['category']['id'])
                qb.join('threats_categories tc', 'tc.threat_id', 't.id')
            if search['threatName']:
                qb.where('t.name', search['threatName'], qb.LIKE)
        where, join = itemgetter('where', 'join')(qb.build())

        query = f"""
        SELECT t.*, JSON_GROUP_ARRAY(c.name) AS categories
        FROM (
            SELECT t.id, t.name, COUNT(*) AS detected
            FROM threat t, file f {join}
            WHERE f.threat_id = t.id {where}
            GROUP BY t.id
            ORDER BY detected DESC
            LIMIT 100
        ) t, threat_category c, threats_categories tc
        WHERE tc.threat_id = t.id AND tc.threat_category_id = c.id
        GROUP BY t.id
        ORDER BY detected DESC
        """

        rows = self.db.fetchAll(query)
        self.beginResetModel()
        self.threats.clear()
        for row in rows:
            row['categories'] = json.loads(row['categories'])
            self.threats.append(row)
        self.endResetModel()
