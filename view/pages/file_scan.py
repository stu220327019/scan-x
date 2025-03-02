from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem, QHeaderView
from PySide6.QtGui import QIcon
import asyncio
from qasync import asyncSlot
import time
import hashlib
import vt
import os
import json
import sqlite3
from pprint import pprint
from functools import partial

from model import FileScanModel, DirScanModel
from model.dir_scan import _FileSystemModelLiteItem
from lib.entity import (FileScanResult, Analysis, Threat,ThreatCategory,
                        ThreatTag, FileType, FileTypeTag)
from view.ui.ui_main import Ui_MainWindow
from widgets import FileScanResultContainer
from core.config import VIRUS_TOTAL_API_KEY, NUM_SCAN_WORKERS
from core import DB
from .base import Base
from pprint import pprint


def get_dir_tree(filepath):
    for root, dirs, files in os.walk(filepath):
        dir_content = []
        for dir in dirs:
            go_inside = os.path.join(filepath, dir)
            dir_content.append(get_dir_tree(go_inside))
        files_lst = []
        for f in files:
            files_lst.append(f)
        _, name = os.path.split(str(root))
        return {'name': name, 'files': files_lst, 'dirs': dir_content, 'root': root}


def build_tree_widget_items(tree):
    items = []
    for d in tree.get('dirs'):
        item = QTreeWidgetItem([d.get('name')])
        item.addChildren(build_tree_widget_items(d))
        items.append(item)
    for f in tree.get('files'):
        item = QTreeWidgetItem([f])
        items.append(item)
    return items



class FileScan(Base):
    fileScanModel = FileScanModel()
    fileScanQueue = asyncio.Queue()
    fileScanWorkerTasks = []

    dirScanQueue = asyncio.Queue()
    dirScanWorkerTasks = []

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_fileScanList.setModel(self.fileScanModel)
        self.ui.tbl_fileScanList.setColumnWidth(0, 300)
        self.ui.tbl_fileScanList.setColumnWidth(1, 150)
        self.ui.btn_dirScan.setEnabled(False)

    def connectSlotsAndSignals(self):
        self.ui.btn_fileSelect.clicked.connect(self.fileBrowse)
        self.ui.fileScanDrop.dropSignal.connect(self.filesDropped)
        self.ui.tbl_fileScanList.doubleClicked.connect(self.filelistItemClick)
        self.ui.tbl_fileScanList.keyPressed.connect(self.filelistkeyPressed)
        self.ui.btn_startFileScan.clicked.connect(self.startFileScan)
        self.ui.btn_stopFileScan.clicked.connect(self.cancelFileScan)
        self.ui.btn_browseDir.clicked.connect(self.dirBrowse)
        self.ui.btn_dirScan.clicked.connect(self.startDirScan)
        self.ui.tbl_dirScan.doubleClicked.connect(self.filelistItemClick)

    def fileBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if dlg.exec_():
            selectedFiles = dlg.selectedFiles()
            for filepath in selectedFiles:
                self.fileScanModel.addItem(filepath)

    def filesDropped(self, filepaths):
        for filepath in filepaths:
            if os.path.isfile(filepath):
                self.fileScanModel.addItem(filepath)

    def dirBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            selectedDir = dlg.selectedFiles()[0]
            self.ui.label_dirSelected.setText(selectedDir)
            self.ui.label_dirSelected.setStyleSheet("color: #7082b6")
            self.ui.btn_dirScan.setEnabled(True)
            dir_tree = get_dir_tree(selectedDir)
            self.dirScanModel = DirScanModel(dir_tree)
            self.ui.tbl_dirScan.setModel(self.dirScanModel)
            self.ui.tbl_dirScan.expandAll()
            # self.ui.tbl_dirScan.resizeColumnToContents(0)
            self.ui.tbl_dirScan.setColumnWidth(0, 300)
            self.dirScanItemMap = {}

            def buildMap(index: QModelIndex, model: DirScanModel, itemMap: dict):
                if not index.isValid():
                    return

                rows = model.rowCount(index)
                cols = model.columnCount(index)

                item = index.internalPointer()
                if item.data():
                    itemMap[item] = index

                for i in range(rows):
                    for j in range(cols):
                        childIndex = model.index(i, j, index)
                        buildMap(childIndex, model, itemMap)

            for i in range(self.dirScanModel.rowCount()):
                buildMap(self.dirScanModel.index(i, 0), self.dirScanModel, self.dirScanItemMap)

    def filelistkeyPressed(self, event):
        if event.key() == Qt.Key_Delete:
            selectedIndexes = self.ui.tbl_fileScanList.selectedIndexes()
            rows = sorted(list(set([index.row() for index in selectedIndexes if index.isValid()])), reverse=True)
            for row in rows:
                self.fileScanModel.removeItem(row)

    def filelistItemClick(self, index: QModelIndex):
        result = index.internalPointer()
        if type(result) == _FileSystemModelLiteItem:
            result = result.data()
        if result:
            self.signals['openRightBox'].emit(result.file.filename, FileScanResultContainer, {'scanResult': result})

    # @asyncSlot()
    def startFileScan(self):
        for row in range(self.fileScanModel.rowCount()):
            index = self.fileScanModel.index(row, 0)
            item = index.internalPointer()
            if item.status in (FileScanResult.STATUS_PENDING, FileScanResult.STATUS_FAILED):
                self.fileScanQueue.put_nowait(index)
                self.fileScanModel.updateItem(index, status=FileScanResult.STATUS_QUEUED)

        if len(self.fileScanWorkerTasks) == 0:
            for i in range(NUM_SCAN_WORKERS):
                worker = FileScanWorker(self.fileScanQueue, VIRUS_TOTAL_API_KEY)
                worker.started.connect(partial(self.workerStarted, self.fileScanModel))
                worker.finished.connect(partial(self.workerFinished, self.fileScanModel))
                worker.error.connect(partial(self.workerError, self.fileScanModel))
                task = asyncio.create_task(worker.run())
                self.fileScanWorkerTasks.append(task)

    def cancelFileScan(self):
        for row in range(self.fileScanModel.rowCount()):
            index = self.fileScanModel.index(row, 0)
            item = index.internalPointer()
            if item.status == FileScanResult.STATUS_QUEUED:
                self.fileScanModel.updateItem(index, status=FileScanResult.STATUS_CANCELED)

    def startDirScan(self):
        self.ui.btn_browseDir.setEnabled(False)
        self.ui.btn_dirScan.setText('Stop')
        self.ui.btn_dirScan.setIcon(QIcon(":/resources/images/icons/rectangle_white.svg"))
        self.ui.btn_dirScan.clicked.disconnect()
        self.ui.btn_dirScan.clicked.connect(self.stopDirScan)
        for index in self.dirScanItemMap.values():
            item = index.internalPointer()
            if item.data().status in (FileScanResult.STATUS_PENDING, FileScanResult.STATUS_FAILED):
                self.dirScanQueue.put_nowait(index)
                self.dirScanModel.updateItem(index, status=FileScanResult.STATUS_QUEUED)

        if len(self.dirScanWorkerTasks) == 0:
            for i in range(NUM_SCAN_WORKERS):
                worker = FileScanWorker(self.dirScanQueue, VIRUS_TOTAL_API_KEY)
                worker.started.connect(partial(self.workerStarted, self.dirScanModel))
                worker.finished.connect(partial(self.workerFinished, self.dirScanModel))
                worker.error.connect(partial(self.workerError, self.dirScanModel))
                task = asyncio.create_task(worker.run())
                self.dirScanWorkerTasks.append(task)

    def stopDirScan(self):
        self.ui.btn_browseDir.setEnabled(True)
        self.ui.btn_dirScan.setText('Start')
        self.ui.btn_dirScan.setIcon(QIcon(":/resources/images/icons/play_white.svg"))
        self.ui.btn_dirScan.clicked.disconnect()
        self.ui.btn_dirScan.clicked.connect(self.startDirScan)
        for index in self.dirScanItemMap.values():
            if index.internalPointer().data().status == FileScanResult.STATUS_QUEUED:
                self.dirScanModel.updateItem(index, status=FileScanResult.STATUS_CANCELED)

    def checkDirScanFinished(self):
        if all(index.internalPointer().data().status != FileScanResult.STATUS_QUEUED
               for index in self.dirScanItemMap.values()):
            self.stopDirScan()

    def workerStarted(self, model, index: QModelIndex):
        model.updateItem(index, status=FileScanResult.STATUS_SCANNING, startedTime=time.time())

    def workerFinished(self, model, index: QModelIndex, scanResult: dict):
        analysis, threat, fileType = scanResult.get('analysis'), scanResult.get('threat'), scanResult.get('fileType')
        analysisStats = analysis.stats
        analysisResults = analysis.results.values()
        detection = [x for x in analysisResults if x['result'] is not None]
        status = FileScanResult.STATUS_COMPLETED if len(detection) == 0 else FileScanResult.STATUS_INFECTED
        result = index.internalPointer()
        if type(result) == _FileSystemModelLiteItem:
            result = result.data()
        file = result.file
        if threat:
            file.threat = threat
        if fileType:
            file.fileType = fileType
        result = model.updateItem(index, file=file, status=status, analysis=analysis, finishedTime=time.time())
        if type(result) == _FileSystemModelLiteItem:
            result = result.data()
        try:
            self.db.beginTransaction()
            fileId = self.db.fetchOneCol(
                'SELECT id FROM file WHERE filepath = ? AND sha1 = ?',
                [file.filepath, file.sha1]
            )
            if not fileId:
                fileTypeId = None
                if file.fileType:
                    fileTypeId = self.db.fetchOneCol('SELECT id FROM file_type WHERE description = ?', [file.fileType.description])
                    if not fileTypeId:
                        cur = self.db.exec('INSERT INTO file_type (description, extension) VALUES (?, ?)',
                                           [file.fileType.description, file.fileType.extension])
                        fileTypeId = cur.lastrowid
                    for tag in file.fileType.tags:
                        tagId = self.db.fetchOneCol('SELECT id FROM file_type_tag WHERE name = ?', [tag.name])
                        if not tagId:
                            cur = self.db.exec('INSERT INTO file_type_tag (name) VALUES (?)', [tag.name])
                            tagId = cur.lastrowid
                        self.db.exec('INSERT INTO file_types_tags (file_type_id, file_type_tag_id) VALUES (?, ?)', [fileTypeId, tagId])
                threatId = None
                if file.threat:
                    threatId = self.db.fetchOneCol('SELECT id FROM threat WHERE name = ?', [file.threat.name])
                    if not threatId:
                        cur = self.db.exec('INSERT INTO threat (name) VALUES (?)', [file.threat.name])
                        threatId = cur.lastrowid
                        for cat in file.threat.categories:
                            catId = self.db.fetchOneCol('SELECT id FROM threat_category WHERE name = ?', [cat.name])
                            if not catId:
                                cur = self.db.exec('INSERT INTO threat_category (name) VALUES (?)', [cat.name])
                                catId = cur.lastrowid
                            self.db.exec('INSERT INTO threats_categories (threat_id, threat_category_id) VALUES (?, ?)', [threatId, catId])
                        for tag in file.threat.tags:
                            tagId = self.db.fetchOneCol('SELECT id FROM threat_tag WHERE name = ?', [tag.name])
                            if not tagId:
                                cur = self.db.exec('INSERT INTO threat_tag (name) VALUES (?)', [tag.name])
                                tagId = cur.lastrowid
                            self.db.exec('INSERT INTO threats_tags (threat_id, threat_tag_id) VALUES (?, ?)', [threatId, tagId])
                cur = self.db.exec("""
                INSERT INTO file (file_type_id, threat_id, filename, filepath, path, sha1, sha256, md5, size, type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                                   [fileTypeId, threatId, file.filename, file.filepath, file.path,
                                    file.sha1, file.sha256, file.md5,
                                    file.size, file.type, time.time()])
                fileId = cur.lastrowid
            cur = self.db.exec("""
            INSERT INTO file_scan_result (file_id, analysis_stats, analysis_results, clean, started_at, finished_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                         [fileId,
                          json.dumps(dict(analysisStats)),
                          json.dumps([dict(res) for res in analysisResults]),
                          len(detection) == 0, result.startedTime, result.finishedTime, time.time()])
            scanResultId = cur.lastrowid
            for analysisResult in analysisResults:
                engineName, virusName = analysisResult.get('engine_name'), analysisResult.get('result')
                engineId = self.db.fetchOneCol('SELECT id FROM engine WHERE name = ?',[engineName])
                virusId = None
                if not engineId:
                    cur = self.db.exec('INSERT INTO engine (name) VALUES (?)', [engineName])
                    engineId = cur.lastrowid
                if virusName:
                    virusId = self.db.fetchOneCol('SELECT id FROM virus WHERE name = ?',[virusName])
                    if not virusId:
                        cur = self.db.exec('INSERT INTO virus (name) VALUES (?)', [virusName])
                        virusId = cur.lastrowid
                self.db.exec("""
                INSERT INTO analysis (engine_id, virus_id, category, type, file_scan_result_id)
                VALUES (?, ?, ?, ?, ?)
                """, [engineId, virusId, analysisResult.get('category'), 'file', scanResultId])
            self.db.commit()
            if type(model) == DirScanModel:
                self.checkDirScanFinished()
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            self.db.rollback()

    def workerError(self, model, index: QModelIndex, error):
        model.updateItem(index, status=FileScanResult.STATUS_FAILED, error=error)

class FileScanWorker(QObject):
    started = Signal(object)
    finished = Signal(object, object)
    error = Signal(object, object)

    def __init__(self, queue, virustotalApiKey, parent=None):
        super(FileScanWorker, self).__init__(parent)
        self.queue = queue
        self.virustotalApiKey = virustotalApiKey

    async def run(self):
        while True:
            try:
                index: QModelIndex = await self.queue.get()
                result: FileScanResult = index.internalPointer()
                if type(result) == _FileSystemModelLiteItem:
                    result = result.data()
                filepath, status = result.id, result.status
                if status == FileScanResult.STATUS_QUEUED:
                    self.started.emit(index)
                    with open(filepath, 'rb') as f:
                        sha1 = hashlib.sha1(f.read()).hexdigest()
                        analysis = None
                        scanResult = None
                        async with vt.Client(self.virustotalApiKey) as client:
                            try:
                                analysis = await client.get_object_async('/files/{}', sha1)
                                scanResult = {
                                    'analysis': Analysis({
                                        'stats': analysis.last_analysis_stats,
                                        'results': analysis.last_analysis_results
                                    })
                                }
                            except vt.APIError as e:
                                if e.code == 'NotFoundError':
                                    analysis = await client.scan_file_async(f, wait_for_completion=True)
                                    scanResult = {
                                        'analysis': Analysis({
                                            'stats': analysis.stats,
                                            'results': analysis.results
                                        })
                                    }
                                else:
                                    raise e
                            threat = analysis.get('popular_threat_classification')
                            if threat:
                                scanResult['threat'] = Threat({
                                    'name': threat.get('suggested_threat_label'),
                                    'categories': [ThreatCategory({'name': cat['value']}) for cat in threat.get('popular_threat_category', [])],
                                    'tags': [ThreatTag({'name': tag['value']}) for tag in threat.get('popular_threat_name', [])]
                                })
                            if analysis.get('type_description'):
                                scanResult['fileType'] = FileType({
                                    'description': analysis.get('type_description'),
                                    'extension': analysis.get('type_extension'),
                                    'tags': [FileTypeTag({'name': tag}) for tag in analysis.get('type_tags', [])]
                                })
                            self.finished.emit(index, scanResult)
                            self.queue.task_done()
                else:
                    self.queue.task_done()
            except Exception as e:
                self.error.emit(index, e)
                self.queue.task_done()
