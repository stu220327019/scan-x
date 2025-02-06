from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
import asyncio
from qasync import asyncSlot
import time
import hashlib
import vt
import os
import json
import sqlite3

from model import FileScanModel
from lib.entity import FileScanResult, Analysis
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer
from core.config import VIRUS_TOTAL_API_KEY, NUM_SCAN_WORKERS
from core import DB
from .base import Base

class FileScan(Base):
    model = FileScanModel()
    queue = asyncio.Queue()
    workerTasks = []

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')
        super().__init__(*args, **kwargs)

    def uiDefinitions(self):
        self.ui.tbl_fileScanList.setModel(self.model)
        self.ui.tbl_fileScanList.setColumnWidth(0, 300)
        self.ui.tbl_fileScanList.setColumnWidth(1, 150)

    def connectSlotsAndSignals(self):
        self.ui.btn_fileSelect.clicked.connect(self.fileBrowse)
        self.ui.fileScanDrop.dropSignal.connect(self.filesDropped)
        self.ui.tbl_fileScanList.doubleClicked.connect(self.filelistItemClick)
        self.ui.tbl_fileScanList.keyPressed.connect(self.filelistkeyPressed)
        self.ui.btn_startFileScan.clicked.connect(self.startFileScan)
        self.ui.btn_stopFileScan.clicked.connect(self.cancelFileScan)

    def fileBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if dlg.exec_():
            selectedFiles = dlg.selectedFiles()
            for filepath in selectedFiles:
                self.model.addFile(filepath)

    def filesDropped(self, filepaths):
        for filepath in filepaths:
            if os.path.isfile(filepath):
                self.model.addFile(filepath)

    def filelistkeyPressed(self, event):
        if event.key() == Qt.Key_Delete:
            selectedIndexes = self.ui.tree_filelist.selectedIndexes()
            rows = sorted(list(set([index.row() for index in selectedIndexes if index.isValid()])), reverse=True)
            for row in rows:
                self.model.removeResult(row)

    def filelistItemClick(self, index: QModelIndex):
        result = self.model.results[index.row()]
        self.signals['openRightBox'].emit(result.file.filename, FileDetailsContainer, {'scanResult': result})

    # @asyncSlot()
    def startFileScan(self):
        files = [f for f in self.model.results
                 if f.status in (FileScanResult.STATUS_PENDING, FileScanResult.STATUS_FAILED)]
        for f in files:
            self.queue.put_nowait(f)
            self.model.updateResult(f.id, status=FileScanResult.STATUS_QUEUED)

        if len(self.workerTasks) == 0:
            for i in range(NUM_SCAN_WORKERS):
                worker = FileScanWorker(self.queue, VIRUS_TOTAL_API_KEY)
                worker.started.connect(self.workerStarted)
                worker.finished.connect(self.workerFinished)
                worker.error.connect(self.workerError)
                task = asyncio.create_task(worker.run())
                self.workerTasks.append(task)

    def cancelFileScan(self):
        files = [f for f in self.model.results
                 if f.status == FileScanResult.STATUS_QUEUED]
        for f in files:
            self.model.updateResult(f.id, status=FileScanResult.STATUS_CANCELED)

    def workerStarted(self, filepath):
        self.model.updateResult(filepath, status=FileScanResult.STATUS_SCANNING, startedTime=time.time())

    def workerFinished(self, filepath, analysis: Analysis):
        analysisStats = analysis.stats
        analysisResults = analysis.results.values()
        detection = [x for x in analysisResults if x['result'] is not None]
        status = FileScanResult.STATUS_COMPLETED if len(detection) == 0 else FileScanResult.STATUS_INFECTED
        result = self.model.updateResult(filepath, status=status, analysis=analysis, finishedTime=time.time())
        file = result.file
        try:
            self.db.beginTransaction()
            fileId = self.db.fetchOneCol(
                'SELECT id FROM file WHERE filepath = ? AND sha1 = ?',
                [file.filepath, file.sha1]
            )
            if not fileId:
                cur = self.db.exec("""
                INSERT INTO file (filename, filepath, path, sha1, sha256, md5, size, type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                                   [file.filename, file.filepath, file.path,
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
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            self.db.rollback()

    def workerError(self, filepath, error):
        self.model.updateResult(filepath, status=FileScanResult.STATUS_FAILED, error=error)

class FileScanWorker(QObject):
    started = Signal(str)
    finished = Signal(str, object)
    error = Signal(str, object)

    def __init__(self, queue, virustotalApiKey, parent=None):
        super(FileScanWorker, self).__init__(parent)
        self.queue = queue
        self.virustotalApiKey = virustotalApiKey

    async def run(self):
        while True:
            try:
                result: FileScanResult = await self.queue.get()
                filepath, status = result.id, result.status
                if status == FileScanResult.STATUS_QUEUED:
                    self.started.emit(filepath)
                    with open(filepath, 'rb') as f:
                        sha1 = hashlib.sha1(f.read()).hexdigest()
                        async with vt.Client(self.virustotalApiKey) as client:
                            try:
                                analysis = await client.get_object_async('/files/{}', sha1)
                                self.finished.emit(filepath, Analysis({
                                    'stats': analysis.last_analysis_stats,
                                    'results': analysis.last_analysis_results
                                }))
                            except vt.APIError as e:
                                if e.code == 'NotFoundError':
                                    analysis = await client.scan_file_async(f, wait_for_completion=True)
                                    self.finished.emit(filepath, Analysis(analysis))
                                else:
                                    raise e
                            self.queue.task_done()
                else:
                    self.queue.task_done()
            except Exception as e:
                self.error.emit(filepath, e)
                self.queue.task_done()
