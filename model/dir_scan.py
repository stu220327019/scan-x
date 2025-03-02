import os
import posixpath, mimetypes
import time
from typing import Any, List, Union
import hashlib

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileIconProvider
from PySide6.QtGui import QColor

from lib.entity import FileScanResult, File, Color
from lib.utils import sizeof_fmt

FSMItemOrNone = Union["_FileSystemModelLiteItem", None]


class _FileSystemModelLiteItem(object):
    """Represents a single node (drive, folder or file) in the tree"""

    def __init__(
        self,
        cols: List[Any],
        icon = QFileIconProvider.Computer,
        parent: FSMItemOrNone = None,
        data = None
    ):
        self._cols: List[Any] = cols
        self._icon = icon
        self._parent: _FileSystemModelLiteItem = parent
        self._data = data
        self.child_items: List[_FileSystemModelLiteItem] = []

    def append_child(self, child: "_FileSystemModelLiteItem"):
        self.child_items.append(child)

    def child(self, row: int) -> FSMItemOrNone:
        try:
            return self.child_items[row]
        except IndexError:
            return None

    def child_count(self) -> int:
        return len(self.child_items)

    def column_count(self) -> int:
        return len(self._cols)

    def col(self, column: int) -> Any:
        try:
            return self._cols[column]
        except IndexError:
            return None

    def set_col(self, column: int, val: Any) -> Any:
        try:
            self._cols[column] = val
        except IndexError:
            return None

    def icon(self):
        return self._icon

    def data(self):
        return self._data

    def update_data(self, **kwargs):
        for k, v in kwargs.items():
            self._data[k] = v

    def row(self) -> int:
        if self._parent:
            return self._parent.child_items.index(self)
        return 0

    def parent_item(self) -> FSMItemOrNone:
        return self._parent


class DirScanModel(QAbstractItemModel):
    def __init__(self, dir_tree: List, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._icon_provider = QFileIconProvider()

        self._root_item = _FileSystemModelLiteItem(
            ["Name", "Size", "Type", "Status"]
        )
        self._setup_model_data(dir_tree, self._root_item)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        item: _FileSystemModelLiteItem = index.internalPointer()
        col = index.column()
        if col == 3:
            val = item.col(col)
            if role == Qt.DisplayRole:
                if val == FileScanResult.STATUS_INFECTED:
                    detection = [x for x in item.data().analysis.results.values() if x['result'] is not None]
                    return val.format(len(detection))
                elif val == FileScanResult.STATUS_FAILED:
                    return val.format(str(item.data().error))
                else:
                    return val
            elif role == Qt.ForegroundRole:
                def getColor(status):
                    if status == FileScanResult.STATUS_COMPLETED:
                        return Color.SUCCESS
                    # elif status == File.STATUS_ATTENTION:
                    #     return Color.WARNING
                    elif status in [FileScanResult.STATUS_FAILED, FileScanResult.STATUS_INFECTED]:
                        return Color.DANGER
                    else:
                        return Color.INFO
                return QColor(getColor(val))
        elif role == Qt.DisplayRole:
            return item.col(col)
        elif col == 0 and role == Qt.DecorationRole:
            return self._icon_provider.icon(item.icon())
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index)

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root_item.col(section)
        return None

    def index(
        self, row: int, column: int, parent: QModelIndex = QModelIndex()
    ) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: _FileSystemModelLiteItem = index.internalPointer()
        parent_item: FSMItemOrNone = child_item.parent_item()

        if parent_item == self._root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self._root_item.column_count()

    def _setup_model_data(
        self, dir_tree, parent: "_FileSystemModelLiteItem"
    ):
        def _process_dir_tree(_dir_tree, _parent: "_FileSystemModelLiteItem"):
            icon = QFileIconProvider.Folder
            cols = [_dir_tree['name'], '', '', '']
            current = _FileSystemModelLiteItem(cols, icon=icon, parent=_parent)
            _parent.append_child(current)
            for dir in _dir_tree['dirs']:
                _process_dir_tree(dir, current)
            for filename in _dir_tree['files']:
                filepath = os.path.join(_dir_tree['root'], filename)
                # file_record = {
                #     "size": sizeof_fmt(osp.getsize(filepath)),
                #     "modified_at": time.strftime(
                #         "%a, %d %b %Y %H:%M:%S %Z", time.localtime(osp.getmtime(filepath))
                #     ),
                #     "type": mimetypes.guess_type(filepath)[0],
                #     'status': 'added'
                # }

                with open(filepath, 'rb') as f:
                    cfile = f.read()
                    file_scan_result = FileScanResult({
                        'file': File({
                            'filepath': filepath,
                            'filename': filename,
                            'path': _dir_tree['root'],
                            'md5': hashlib.md5(cfile).hexdigest(),
                            'sha1': hashlib.sha1(cfile).hexdigest(),
                            'sha256': hashlib.sha256(cfile).hexdigest(),
                            'size': os.path.getsize(filepath),
                            'type': mimetypes.guess_type(filepath)[0]
                        }),
                        'status': FileScanResult.STATUS_PENDING,
                        'id': filepath
                    })

                icon = QFileIconProvider.File
                cols = [
                    filename,
                    sizeof_fmt(file_scan_result.file.size),
                    file_scan_result.file.type,
                    # file_record["modified_at"],
                    file_scan_result.status
                ]
                item = _FileSystemModelLiteItem(cols, icon=icon, parent=current, data=file_scan_result)
                current.append_child(item)

        _process_dir_tree(dir_tree, parent)

    def updateItem(self, index: QModelIndex, **kwargs) -> FileScanResult:
        item = index.internalPointer()
        item.update_data(**kwargs)
        if 'status' in kwargs:
            item.set_col(3, kwargs.get('status'))
        row = index.row()
        top_left = self.index(row, 0)
        bottom_right = self.index(row, 3)
        self.dataChanged.emit(top_left, bottom_right)
        return item
