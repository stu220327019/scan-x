from PySide6.QtCore import QThread, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import Qt, QIcon, QColor
import hashlib
import magic
import os

from lib.entity import File, FileScanResult, Color

class FileScanModel(QAbstractTableModel):
    results: list[FileScanResult] = []
    added = set()

    def __init__(self, parent=None):
        super().__init__(parent)

    def rowCount(self, parent=QModelIndex()):
        return len(self.results) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Path, Filename, Status

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.DecorationRole, Qt.ForegroundRole):
            return None
        row = index.row()
        col = index.column()

        result = self.results[row]

        if role == Qt.DisplayRole:
            if col == 2:
                status = result.status
                if status == FileScanResult.STATUS_INFECTED:
                    detection = [x for x in result.analysis.results.values() if x['result'] is not None]
                    return status.format(len(detection))
                elif status == FileScanResult.STATUS_FAILED:
                    return status.format(str(result.error))
                else:
                    return status
            else:
                return result.file.get(['path', 'filename'][col])
        elif role == Qt.DecorationRole:
            if col == 2:
                def getIcon(status):
                    if status == FileScanResult.STATUS_COMPLETED:
                        return ':/resources/images/icons/check-circle.svg'
                    # elif status == File.STATUS_ATTENTION:
                    #     return ':/resources/images/icons/alert-triangle.svg'
                    elif status in [FileScanResult.STATUS_FAILED, FileScanResult.STATUS_INFECTED]:
                        return ':/resources/images/icons/exclaimation-circle.svg'
                    else:
                        return ':/resources/images/icons/info-circle.svg'
                return QIcon(getIcon(result.status))
            else:
                return None
        elif role == Qt.ForegroundRole:
            if col == 2:
                def getColor(status):
                    if status == FileScanResult.STATUS_COMPLETED:
                        return Color.SUCCESS
                    # elif status == File.STATUS_ATTENTION:
                    #     return Color.WARNING
                    elif status in [FileScanResult.STATUS_FAILED, FileScanResult.STATUS_INFECTED]:
                        return Color.DANGER
                    else:
                        return Color.INFO
                return QColor(getColor(result.status))
            else:
                return None

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
                self.results.append(FileScanResult({
                    'file': File({
                        'filepath': filepath,
                        'filename': filename,
                        'path': path,
                        'md5': hashlib.md5(cfile).hexdigest(),
                        'sha1': hashlib.sha1(cfile).hexdigest(),
                        'sha256': hashlib.sha256(cfile).hexdigest(),
                        'size': os.path.getsize(filepath),
                        'type': magic.from_file(filepath)
                    }),
                    'status': FileScanResult.STATUS_PENDING,
                    'id': filepath
                }))
                self.endInsertRows()
                self.added.add(filepath)
            # fileDetailsThread = FileDetailsThread(filepath)
            # fileDetailsThread.loaded.connect(self.updateFileInfo)
            # fileDetailsThread.start()

    # def updateFileInfo(self, fileInfo: dict):
    #     print(fileInfo)

    def getResultRow(self, id):
        return next(iter([i for i, j in enumerate(self.results) if j['id'] == id]), None)

    def getResult(self, id) -> FileScanResult:
        row = self.getResultRow(id)
        if row is not None:
            return self.results[row]

    def updateResult(self, id, **kwargs) -> FileScanResult:
        row = self.getResultRow(id)
        if row is not None:
            result = self.results[row]
            for k, w in kwargs.items():
                result[k] = w
            self.results[row] = result
            top_left = self.index(row, 0)
            bottom_right = self.index(row, 2)
            self.dataChanged.emit(top_left, bottom_right)
            return result
        return False

    def removeResult(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        result = self.results[row]
        del self.results[row]
        self.added.remove(result.id)
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
            _, filename  = os.pat1h.split(str(filepath))
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
