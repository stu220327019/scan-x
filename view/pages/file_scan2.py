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

from model import FileScanModel, File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer
from core.config import VIRUS_TOTAL_API_KEY, NUM_SCAN_WORKERS
from core import DB

class FileScan2(QObject):
    model = FileScanModel()
    files = []
    queue = asyncio.Queue()
    workerTasks = []

    def __init__(self, ui: Ui_MainWindow, signals=None, ctx=None, *args, **kwargs):
        super().__init__()
        self.ui = ui
        self.signals = signals
        self.db: DB = ctx.get('db')

        self.uiDefinitions()
        self.connect_slots_and_signals()

    def uiDefinitions(self):
        self.ui.tree_filelist.setModel(self.model)
        self.ui.tree_filelist.setColumnWidth(0, 300)
        self.ui.tree_filelist.setColumnWidth(1, 150)

    def connect_slots_and_signals(self):
        self.ui.btn_fileSelect.clicked.connect(self.fileBrowse)
        self.ui.fileScanDrop.dropSignal.connect(self.filesDropped)
        self.ui.tree_filelist.doubleClicked.connect(self.filelistItemClick)
        self.ui.tree_filelist.keyPressed.connect(self.filelistkeyPressed)
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
                self.model.removeFile(row)

    def filelistItemClick(self, index: QModelIndex):
        row = index.row()
        fileInfo = self.model.files[row]
        self.signals['openRightBox'].emit(fileInfo.get('filename'), FileDetailsContainer, {'fileInfo': fileInfo})

    # @asyncSlot()
    def startFileScan(self):
        files = [f for f in self.model.files
                 if f.get('status') in (File.STATUS_PENDING, File.STATUS_FAILED)]
        for f in files:
            self.queue.put_nowait(f)
            self.model.updateFile(f.get('filepath'), status=File.STATUS_QUEUED)

        if len(self.workerTasks) == 0:
            for i in range(NUM_SCAN_WORKERS):
                worker = FileScanWorker(self.queue, VIRUS_TOTAL_API_KEY)
                worker.started.connect(self.workerStarted)
                worker.finished.connect(self.workerFinished)
                worker.error.connect(self.workerError)
                task = asyncio.create_task(worker.run())
                self.workerTasks.append(task)

    def cancelFileScan(self):
        files = [f for f in self.model.files
                 if f.get('status') == File.STATUS_QUEUED]
        for f in files:
            self.model.updateFile(f.get('filepath'), status=File.STATUS_CANCELED)

    def workerStarted(self, filepath):
        self.model.updateFile(filepath, status=File.STATUS_SCANNING, startedTime=time.time())

    def workerFinished(self, filepath, analysis):
        analysisStats = analysis.get('stats')
        analysisResults = analysis.get('results').values()
        detection = [x for x in analysisResults if x['result'] is not None]
        status = File.STATUS_COMPLETED if len(detection) == 0 else File.STATUS_INFECTED
        file = self.model.updateFile(filepath, status=status, analysisResults=analysisResults, finishedTime=time.time())
        try:
            self.db.beginTransaction()
            fileId = self.db.fetchOneCol(
                'SELECT id FROM file WHERE filepath = ? AND sha1 = ?',
                [file.get('filepath'), file.get('sha1')]
            )
            if not fileId:
                cur = self.db.exec("""
                INSERT INTO file (filename, filepath, path, sha1, sha256, md5, size, type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                                   [file.get('filename'), file.get('filepath'), file.get('path'),
                                    file.get('sha1'), file.get('sha256'), file.get('md5'),
                                    file.get('size'), file.get('type'), time.time()])
                fileId = cur.lastrowid
            cur = self.db.exec("""
            INSERT INTO file_scan_result (file_id, analysis_stats, analysis_results, clean, started_at, finished_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                         [fileId,
                          json.dumps(dict(analysisStats)),
                          json.dumps([dict(res) for res in analysisResults]),
                          len(detection) == 0, file.get('startedTime'), file.get('finishedTime'), time.time()])
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

    def workerError(self, filepath, err):
        self.model.updateFile(filepath, status=File.STATUS_FAILED, err=err)

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
                fileInfo = await self.queue.get()
                filepath, status = fileInfo.get('filepath'), fileInfo.get('status')
                if status == File.STATUS_QUEUED:
                    self.started.emit(filepath)
                    with open(filepath, 'rb') as f:
                        sha1 = hashlib.sha1(f.read()).hexdigest()
                        async with vt.Client(self.virustotalApiKey) as client:
                            try:
                                analysis = await client.get_object_async('/files/{}', sha1)
                                self.finished.emit(filepath, {
                                    'stats': analysis.last_analysis_stats,
                                    'results': analysis.last_analysis_results
                                })
                            except vt.APIError as e:
                                if e.code == 'NotFoundError':
                                    analysis = await client.scan_file_async(f, wait_for_completion=True)
                                    self.finished.emit(filepath, analysis)
                                else:
                                    raise e
                            self.queue.task_done()
                else:
                    self.queue.task_done()
            except Exception as err:
                self.error.emit(filepath, err)
                self.queue.task_done()
