from PySide6.QtCore import QThread, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import Qt, QIcon, QColor
import hashlib
import os
from abc import ABC, abstractmethod
import mimetypes

from lib.entity import File, FileScanResult, Color

class AbstractScanModel(ABC):
    @abstractmethod
    def getItems(self):
        raise NotImplementedError

    @abstractmethod
    def getItem(self, index: QModelIndex):
        raise NotImplementedError

    @abstractmethod
    def updateItem(self, index: QModelIndex, **kwargs):
        raise NotImplementedError


class FileScanModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data: list[FileScanResult] = []
        self._added = set()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Path, Filename, Status

    def index(
        self, row: int, column: int, parent: QModelIndex = QModelIndex()
    ) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        item = self._data[row]
        if item:
            return self.createIndex(row, column, item)
        return QModelIndex()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.DecorationRole, Qt.ForegroundRole):
            return None
        row = index.row()
        col = index.column()

        result: FileScanResult = index.internalPointer()

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

    def addItem(self, filepath) -> QModelIndex:
        if not filepath in self._added:
            with open(filepath, 'rb') as f:
                cfile = f.read()
                path, filename  = os.path.split(str(filepath))
                index = QModelIndex()
                self.beginInsertRows(index, self.rowCount(), self.rowCount())
                self._data.append(FileScanResult({
                    'file': File({
                        'filepath': filepath,
                        'filename': filename,
                        'path': path,
                        'md5': hashlib.md5(cfile).hexdigest(),
                        'sha1': hashlib.sha1(cfile).hexdigest(),
                        'sha256': hashlib.sha256(cfile).hexdigest(),
                        'size': os.path.getsize(filepath),
                        'type': mimetypes.guess_type(filepath)[0]
                    }),
                    'status': FileScanResult.STATUS_PENDING,
                    'id': filepath
                }))
                self.endInsertRows()
                self._added.add(filepath)
                return index
            # fileDetailsThread = FileDetailsThread(filepath)
            # fileDetailsThread.loaded.connect(self.updateFileInfo)
            # fileDetailsThread.start()

    def getItems(self):
        return self._data

    def getItem(self, index: QModelIndex):
        return index.internalPointer()

    def updateItem(self, index: QModelIndex, **kwargs) -> FileScanResult:
        item = index.internalPointer()
        for k, v in kwargs.items():
            item[k] = v
        row = index.row()
        top_left = self.index(row, 0)
        bottom_right = self.index(row, 2)
        self.dataChanged.emit(top_left, bottom_right)
        return item

    def removeItem(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        result = self._data[row]
        del self._data[row]
        self._added.remove(result.id)
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
