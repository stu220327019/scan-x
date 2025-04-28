from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor, QIcon
import json

from core import DB

class FileTypeModel(QAbstractTableModel):
    fileTypes = []
    loaded = Signal(list)

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

    def rowCount(self, parent=QModelIndex()):
        return len(self.fileTypes) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Description'][section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole,):
            return None
        row = index.row()
        col = index.column()
        return self.fileTypes[row][['description'][col]]

    def loadData(self, viewBy=None):
        query = """
        SELECT t.id, t.description
        FROM file_type t
        """
        rows = self.db.fetchAll(query)
        self.beginResetModel()
        self.fileTypes.clear()
        for row in rows:
            self.fileTypes.append(row)
        self.endResetModel()
        self.loaded.emit(self.fileTypes)
