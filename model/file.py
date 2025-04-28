from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB, QueryBuilder
from lib.entity import FileScanResult, File, Analysis, Color, Threat, FileType
from lib.utils import sizeof_fmt

class FileModel(QAbstractTableModel):
    def __init__(self, db: DB, parent=None, show_extra_cols=False):
        super().__init__(parent)
        self.db = db
        self.show_extra_cols = show_extra_cols
        self._data: list[File] = []
        self._headers = ['Filename', 'Path', 'Type', 'Threat', 'Size']
        if show_extra_cols:
            self._headers += ['# scanned', 'Last scanned at']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.DecorationRole, Qt.ForegroundRole):
            return None

        row = index.row()
        col = index.column()

        data = self._data[row]

        if role == Qt.DisplayRole:
            val = data['file'][['filename', 'path', 'fileType', 'threat', 'size'][col]] if col < 5 else data[['num_scanned', 'last_scanned_at'][col-5]]
            if col == 2:
                val = val['description'] if val else 'Unknown'
            elif col == 3:
                val = val['name'] if val else 'Clean'
            elif col == 4:
                val = sizeof_fmt(val)
            elif col == 6:
                val = datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S')
            return val
        elif role == Qt.ForegroundRole:
            if col == 3:
                return QColor(Color.SUCCESS if not data['file']['threat'] else Color.DANGER)
            else:
                return None

    def loadData(self, search=None, limit=None):
        query = QueryBuilder()\
            .SELECT('f.*', ('file_id', 'f.id'), ('threat', 't.name'), ('file_type', 'ft.description'))\
            .FROM(('f', 'file'))\
            .LEFT_JOIN('threat t ON t.id = f.threat_id')\
            .LEFT_JOIN('file_type ft on ft.id = f.file_type_id')\
            .ORDER_BY('f.created_at DESC')
        if search:
            if 'threat' in search:
                query.WHERE('t.id = ?')
                query.add_param(search['threat'])
            if  'file_type' in search and search['file_type']:
                query.WHERE('ft.id = ?')
                query.add_param(search['file_type']['id'])
            if 'search' in search and search['search']:
                query.WHERE('(t.name LIKE ? OR f.filename LIKE ?)')
                query.add_param(f'%{search['search']}%')
                query.add_param(f'%{search['search']}%')
        if limit:
            query.LIMIT(limit)

        if self.show_extra_cols:
            subquery = query
            query = QueryBuilder()
            query.add_params(subquery.params())
            query\
                .SELECT(
                    't.*',
                    ('num_scanned', '(%s)' % str(QueryBuilder()\
                     .SELECT('COUNT(*)')\
                     .FROM('file_scan_result')\
                     .WHERE('file_id = t.file_id'))),
                    ('last_scanned_at', '(%s)' % str(QueryBuilder()\
                     .SELECT('MAX(created_at)')\
                     .FROM('file_scan_result')\
                     .WHERE('file_id = t.file_id')))
                )\
                .FROM('t')\
                .WITH(('t', str(subquery)))

        rows = self.db.fetchAll(str(query), query.params())
        self.beginResetModel()
        self._data.clear()
        for row in rows:
            file = File({
                'filename': row['filename'],
                'filepath': row['filepath'],
                'path': row['path'],
                'sha1': row['sha1'],
                'sha256': row['sha256'],
                'md5': row['md5'],
                'size': row['size'],
                'type': row['type'],
                'id': row['file_id'],
                'threat': Threat({'name': row['threat']})
                if row['threat'] else None,
                'fileType': FileType({'description': row['file_type']})
                if row['file_type'] else None
            })
            data = {
                'file': file
            }
            if self.show_extra_cols:
                data['num_scanned'] = row['num_scanned']
                data['last_scanned_at'] = row['last_scanned_at']
            self._data.append(data)
        self.endResetModel()
