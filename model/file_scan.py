from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import os

from .file import File

class FileScanModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.files = []
        self.added = set()

    def rowCount(self, parent=QModelIndex()):
        return len(self.files) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Filename, Path, Status

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        row = index.row()
        col = index.column()

        return self.files[row].get(['path', 'filename', 'status'][col])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Path', 'Filename', 'Status'][section]
        return None

    # def flags(self, index):
    #     return super().flags(index) | Qt.ItemIsEditable

    # def setData(self, index, value, role=Qt.EditRole):
    #     if role != Qt.EditRole or not index.isValid():
    #         return False

    #     row = index.row()
    #     col = index.column()
    #     field = ['first', 'last', 'email'][col]
    #     self.users[row][field] = value
    #     self.dataChanged.emit(index, index)
    #     return True

    def addFile(self, filepath):
        if not filepath in self.added:
            path, filename  = os.path.split(str(filepath))
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.files.append({'filename': filename, 'path': path, 'status': File.STATUS_PENDING})
            self.endInsertRows()
            self.added.add(filepath)

    # def update_user(self, row, first, last, email):
    #     if 0 <= row < self.rowCount():
    #         self.users[row] = {'first': first, 'last': last, 'email': email}
    #         top_left = self.index(row, 0)
    #         bottom_right = self.index(row, 2)
    #         self.dataChanged.emit(top_left, bottom_right)
    #         return True
    #     return False

    def removeRow(self, row, parent=QModelIndex()):
        return self.removeRows(row, 1, parent)

    def removeRows(self, row, count, parent=QModelIndex()):
        if row < 0 or row + count > self.rowCount():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        del self.files[row:row+count]
        self.endRemoveRows()
        return True
