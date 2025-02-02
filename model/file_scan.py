from PySide6.QtCore import Qt, QThread, QAbstractTableModel, QModelIndex, Signal
import hashlib
import magic
import os

from .file import File

class FileScanModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.files = []
        self.fileDetails = {}
        self.fileScanResults = {}
        self.added = set()

    def rowCount(self, parent=QModelIndex()):
        return len(self.files) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Path, Filename, Status

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
            with open(filepath, 'rb') as f:
                cfile = f.read()
                path, filename  = os.path.split(str(filepath))
                self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
                self.files.append({
                    'filepath': filepath,
                    'filename': filename,
                    'path': path,
                    'md5': hashlib.md5(cfile).hexdigest(),
                    'sha1': hashlib.sha1(cfile).hexdigest(),
                    'sha256': hashlib.sha256(cfile).hexdigest(),
                    'size': os.path.getsize(filepath),
                    'type': magic.from_file(filepath),
                    'status': File.STATUS_PENDING
                })
                self.endInsertRows()
                self.added.add(filepath)
            # fileDetailsThread = FileDetailsThread(filepath)
            # fileDetailsThread.loaded.connect(self.updateFileInfo)
            # fileDetailsThread.start()

    # def updateFileInfo(self, fileInfo: dict):
    #     print(fileInfo)


    # def update_user(self, row, first, last, email):
    #     if 0 <= row < self.rowCount():
    #         self.users[row] = {'first': first, 'last': last, 'email': email}
    #         top_left = self.index(row, 0)
    #         bottom_right = self.index(row, 2)
    #         self.dataChanged.emit(top_left, bottom_right)
    #         return True
    #     return False

    def removeFile(self, index):
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        file = self.files[index.row()]
        del self.files[index.row()]
        self.added.remove(file['filepath'])
        self.endRemoveRows()


class FileDetailsThread(QThread):
    loaded = Signal(dict)

    def __init__(self, filepath, parent=None):
        super(FileDetailsThread, self).__init__(parent)
        self.filepath = str(filepath)

    @staticmethod
    def getFileDetails(filepath):
        with open(filepath, 'rb') as f:
            cfile = f.read()
            _, filename  = os.path.split(str(filepath))
            return {
                'name': filename,
                'path': filepath,
                'md5': hashlib.md5(cfile).hexdigest(),
                'sha1': hashlib.sha1(cfile).hexdigest(),
                'sha256': hashlib.sha256(cfile).hexdigest(),
                'size': os.path.getsize(filepath),
                'type': magic.from_file(filepath)
            }

    def run(self):
        fileDetails = FileDetailsThread.getFileDetails(self.filepath)
        self.loaded.emit(fileDetails)
