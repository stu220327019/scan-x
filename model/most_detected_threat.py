from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB
from .file import File
from .color import Color

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

    def loadData(self):
        rows = self.db.fetchAll("""
        SELECT v.name, COUNT(*) AS detected FROM virus v, analysis a
        WHERE a.virus_id = v.id
        GROUP BY v.id
        ORDER BY detected DESC LIMIT 100
        """)
        self.beginResetModel()
        self.threats = []
        for row in rows:
            self.threats.append(row)
        self.endResetModel()
