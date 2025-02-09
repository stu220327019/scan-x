from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB
from lib.entity import UrlScanResult, URL, UrlHttpResponse, Analysis, Color

class UrlScanResultModel(QAbstractTableModel):
    results: list[UrlScanResult] = []

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

    def rowCount(self, parent=QModelIndex()):
        return len(self.results) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return 3  # Filename, Status, Scanned At

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ['URL', 'Status', 'Scanned At'][section]
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
                    status = result.STATUS_SAFE
                else:
                    stats = result.analysis.stats
                    detection = sum([v for k, v in stats.items() if k in ('malicious', 'suspicious')])
                    status = result.STATUS_UNSAFE
                return status
            elif col == 2:
                return datetime.fromtimestamp(result.scannedAt).strftime('%Y-%m-%d %H:%M:%S')
            return result.url.url
        elif role == Qt.DecorationRole:
            if col == 1:
                return QIcon(':/resources/images/icons/check-circle.svg' \
                             if result.get('clean') == True else \
                             ':/resources/images/icons/exclaimation-circle.svg')
            else:
                return None
        elif role == Qt.ForegroundRole:
            if col == 1:
                return QColor(Color.SUCCESS if result.clean == True else Color.DANGER)
            else:
                return None

    def getRow(self, id):
        return next(iter([i for i, j in enumerate(self.results) if j['id'] == id]), None)

    def delScanResult(self, id):
        row = self.getRow(id)
        if row:
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.results[row]
            self.endRemoveRows()
        self.db.exec('DELETE FROM url_scan_result WHERE id = ?', [id], True)

    def loadData(self):
        rows = self.db.fetchAll("""
        SELECT u.url, resp.*, r.id, r.clean, r.analysis_stats, r.analysis_results, r.started_at, r.finished_at, r.created_at
        FROM url_scan_result r, url u
        LEFT JOIN url_http_response resp ON resp.id = r.url_http_response_id
        WHERE u.id = r.url_id
        ORDER BY r.created_at DESC LIMIT 100
        """)
        self.beginResetModel()
        self.results.clear()
        for row in rows:
            result = UrlScanResult({
                'url': URL({
                    'url': row['url'],
                    'httpResponse': UrlHttpResponse({
                        'statusCode': row.get('status_code'),
                        'contentLength': row.get('content_length'),
                        'contentSha256': row.get('content_sha256'),
                        'headers': json.loads(row.get('headers')) if row.get('headers') else None,
                        'title': row.get('title')
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
