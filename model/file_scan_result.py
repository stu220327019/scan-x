from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB, QueryBuilder
from lib.entity import FileScanResult, File, Analysis, Color, Threat, FileType

class FileScanResultModel(QAbstractTableModel):
    def __init__(self, db: DB, parent=None, show_extra_cols=False):
        super().__init__(parent)
        self.db = db
        self.results: list[FileScanResult] = []
        self.show_extra_cols = show_extra_cols

    def rowCount(self, parent=QModelIndex()):
        return len(self.results) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Filename, Status, Scanned At

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['Filename', 'Status', 'Scanned At'][section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.DecorationRole, Qt.ForegroundRole):
            return None

        row = index.row()
        col = index.column()

        result = self.results[row]

        if role == Qt.DisplayRole:
            if col == 1:
                if result.clean == True:
                    status = result.STATUS_CLEAN
                else:
                    stats = result.analysis.stats
                    detection = sum([v for k, v in stats.items() if k in ('malicious', 'suspicious')])
                    status = result.STATUS_INFECTED.format(detection)
                return status
            elif col == 2:
                return datetime.fromtimestamp(result.scannedAt).strftime('%Y-%m-%d %H:%M:%S')
            return result.file.filename
        elif role == Qt.DecorationRole:
            if col == 1:
                return QIcon(':/resources/images/icons/check-circle.png' \
                             if result.clean == True else \
                             ':/resources/images/icons/exclaimation-circle.png')
            else:
                return None
        elif role == Qt.ForegroundRole:
            if col == 1:
                return QColor(Color.SUCCESS if result.clean == True else Color.DANGER)
            else:
                return None

    def fetchFileInfo(self, fileId):
        row = self.db.fetchOne("""
        SELECT t.name AS threat, ft.description AS file_type
        FROM file f
        LEFT JOIN threat t ON t.id = f.threat_id
        LEFT JOIN file_type ft on ft.id = f.file_type_id
        WHERE f.id = ?
        """, [fileId])
        if row:
            return {
                'threat': Threat({
                    'name': row['threat']
                }),
                'fileType': FileType({
                    'description': row['file_type']
                })
            }

    def getRow(self, id):
        return next(iter([i for i, j in enumerate(self.results) if j['id'] == id]), None)

    def delScanResult(self, id):
        row = self.getRow(id)
        if row:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.results[row]
            self.endRemoveRows()
        self.db.exec('DELETE FROM file_scan_result WHERE id = ?', [id], True)


    def loadData(self, search=None, limit=None):
        query = QueryBuilder()\
            .SELECT('f.*', ('file_id', 'f.id'), 'r.id', 'r.clean', 'r.analysis_stats',
                    'r.analysis_results', 'r.started_at', 'r.finished_at', 'r.created_at')\
            .FROM(('r', 'file_scan_result'), ('f', 'file'))\
            .WHERE('f.id = r.file_id')\
            .ORDER_BY('r.created_at DESC')
        if self.show_extra_cols:
            query.SELECT(('threat', 't.name'), ('file_type', 'ft.description'))\
                 .LEFT_JOIN('threat t ON t.id = f.threat_id')\
                 .LEFT_JOIN('file_type ft on ft.id = f.file_type_id')
        if search:
            if 'threat' in search:
                query.WHERE('t.id = ?')
                query.add_param(search['threat'])
            if 'file' in search:
                query.WHERE('f.id = ?')
                query.add_param(search['file'])
        if limit:
            query.LIMIT(limit)
        rows = self.db.fetchAll(str(query), query.params())
        self.beginResetModel()
        self.results.clear()
        for row in rows:
            result = FileScanResult({
                'file': File({
                    'filename': row['filename'],
                    'filepath': row['filepath'],
                    'path': row['path'],
                    'sha1': row['sha1'],
                    'sha256': row['sha256'],
                    'md5': row['md5'],
                    'size': row['size'],
                    'type': row['type'],
                    'id': row['file_id'],
                    'threat': Threat({
                        'name': row['threat'] if 'threat' in row else None
                    }),
                    'fileType': FileType({
                        'description': row['file_type'] if 'file_type' in row else None
                    })
                }),
                'analysis': Analysis({
                    'stats': json.loads(row['analysis_stats']),
                    'results': json.loads(row['analysis_results'])
                }),
                'clean':row['clean'],
                'startedTime': row['started_at'],
                'finishedTime': row['finished_at'],
                'scannedAt': row['created_at'],
                'id': row['id']
            })
            self.results.append(result)
        self.endResetModel()
