from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB

class MostDetectedThreatModel(QAbstractTableModel):
    threats = []

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

    def rowCount(self, parent=QModelIndex()):
        return len(self.threats) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Threat / Virus', 'Detected', 'Detected (Unique)'][section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole,):
            return None
        row = index.row()
        col = index.column()
        return self.threats[row][['name', 'detected'][col]]

    def loadData(self, filterBy):
        query = 'SELECT v.name, COUNT(*) AS detected FROM virus v, analysis a WHERE a.virus_id = v.id'
        query += " AND a.category NOT IN (?, ?)"
        queryParams = ['harmless', 'undetected']
        if filterBy not in (None, 'all'):
            queryParams.append(filterBy)
            query += ' AND a.type = ?'
        query += ' GROUP BY v.id ORDER BY detected DESC LIMIT 100'
        rows = self.db.fetchAll(query, queryParams)
        self.beginResetModel()
        self.threats.clear()
        for row in rows:
            self.threats.append(row)
        self.endResetModel()
