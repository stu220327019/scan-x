from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon
import json
from datetime import datetime

from core import DB
from .file import File
from .color import Color

class FileScanResultModel(QAbstractTableModel):
    results = []

    def __init__(self, db: DB, parent=None):
        super().__init__(parent)
        self.db = db

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
                if result['clean'] == True:
                    status = File.STATUS_CLEAN
                else:
                    stats = result.get('analysisStats')
                    detection = sum([v for k, v in stats.items() if k in ('malicious', 'suspicious')])
                    status = File.STATUS_INFECTED.format(detection)
                return status
            elif col == 2:
                return datetime.fromtimestamp(result.get('created_at')).strftime('%Y-%m-%d %H:%M:%S')
            return result[['filename'][col]]
        elif role == Qt.DecorationRole:
            if col == 1:
                return QIcon(':/resources/images/icons/check-circle.svg' \
                             if result.get('clean') == True else \
                             ':/resources/images/icons/exclaimation-circle.svg')
            else:
                return None
        elif role == Qt.ForegroundRole:
            if col == 1:
                return QColor(Color.SUCCESS if result.get('clean') == True else Color.DANGER)
            else:
                return None

    def loadData(self):
        rows = self.db.fetchAll("""
        SELECT f.*, r.clean, r.analysis_stats, r.analysis_results, r.started_at, r.finished_at, r.created_at FROM file_scan_result r, file f
        WHERE f.id = r.file_id
        ORDER BY r.created_at DESC LIMIT 100
        """)
        self.beginResetModel()
        self.results = []
        for row in rows:
            row['analysisStats'] = json.loads(row['analysis_stats'])
            row['analysisResults'] = json.loads(row['analysis_results'])
            row['startedTime'] = row['started_at']
            row['finishedTime'] = row['finished_at']
            self.results.append(row)
        self.endResetModel()
