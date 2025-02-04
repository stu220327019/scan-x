from PySide6.QtCore import QThread, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import Qt, QIcon, QColor
import hashlib
import magic
import os

from .file import File
from .color import Color

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
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.DecorationRole, Qt.ForegroundRole):
            return None
        row = index.row()
        col = index.column()

        fileInfo = self.files[row]

        if role == Qt.DisplayRole:
            if col == 2:
                status = fileInfo.get('status')
                if status == File.STATUS_INFECTED:
                    results = fileInfo.get('analysis').last_analysis_results.values()
                    detection = [x for x in results if x['result'] is not None]
                    return status.format(len(detection))
                elif status == File.STATUS_FAILED:
                    return status.format(str(fileInfo.get('err')))
                else:
                    return status
            else:
                return fileInfo.get(['path', 'filename'][col])
        elif role == Qt.DecorationRole:
            if col == 2:
                def getIcon(status):
                    if status == File.STATUS_COMPLETED:
                        return ':/resources/images/icons/check-circle.svg'
                    # elif status == File.STATUS_ATTENTION:
                    #     return ':/resources/images/icons/alert-triangle.svg'
                    elif status in [File.STATUS_FAILED, File.STATUS_INFECTED]:
                        return ':/resources/images/icons/exclaimation-circle.svg'
                    else:
                        return ':/resources/images/icons/info-circle.svg'
                return QIcon(getIcon(fileInfo.get('status')))
            else:
                return None
        elif role == Qt.ForegroundRole:
            if col == 2:
                def getColor(status):
                    if status == File.STATUS_COMPLETED:
                        return Color.SUCCESS
                    # elif status == File.STATUS_ATTENTION:
                    #     return Color.WARNING
                    elif status in [File.STATUS_FAILED, File.STATUS_INFECTED]:
                        return Color.DANGER
                    else:
                        return Color.INFO
                return QColor(getColor(fileInfo.get('status')))
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

    def getFileRow(self, filepath):
        return next(iter([i for i, j in enumerate(self.files) if j['filepath'] == filepath]), None)

    def getFile(self, filepath):
        row = self.getFileRow()
        if row is not None:
            return self.files[row]

    def updateFile(self, filepath, **kwargs):
        row = self.getFileRow(filepath)
        if row is not None:
            fileInfo = self.files[row]
            for k, w in kwargs.items():
                fileInfo[k] = w
            self.files[row] = fileInfo
            top_left = self.index(row, 0)
            bottom_right = self.index(row, 2)
            self.dataChanged.emit(top_left, bottom_right)
            return fileInfo
        return False

    def removeFile(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        file = self.files[row]
        del self.files[row]
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
