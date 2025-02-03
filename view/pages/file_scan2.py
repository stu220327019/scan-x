from PySide6.QtCore import QObject, QThread, Signal, Qt, QModelIndex
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
import asyncio
from qasync import asyncSlot
import time
import hashlib
import vt

from model import FileScanModel, File
from view.ui.ui_main import Ui_MainWindow
from widgets import FileDetailsContainer
from core.config import VIRUS_TOTAL_API_KEY, NUM_SCAN_WORKERS

class FileScan2(QObject):
    model = FileScanModel()
    files = []
    queue = asyncio.Queue()
    workerTasks = []

    def __init__(self, ui: Ui_MainWindow, signals=None):
        super().__init__()
        self.ui = ui
        self.signals = signals

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

    def fileBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if dlg.exec_():
            selectedFiles = dlg.selectedFiles()
            for filepath in selectedFiles:
                self.model.addFile(filepath)

    def filesDropped(self, filepaths):
        for filepath in filepaths:
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
                 if f.get('status') == File.STATUS_PENDING]
        for f in files:
            self.queue.put_nowait(f)
            self.model.updateFile(f.get('filepath'), status=File.STATUS_QUEUED)

        if len(self.workerTasks) == 0:
            for i in range(NUM_SCAN_WORKERS):
                worker = FileScanWorker(self.queue, VIRUS_TOTAL_API_KEY)
                worker.started.connect(self.workerStarted)
                worker.finished.connect(self.workerFinished)
                task = asyncio.create_task(worker.run())
                self.workerTasks.append(task)

    def workerStarted(self, filepath):
        self.model.updateFile(filepath, status=File.STATUS_SCANNING, startedTime=time.time())

    def workerFinished(self, filepath, analysis):
        results = analysis.last_analysis_results.values()
        detection = [x for x in results if x['result'] is not None]
        status = File.STATUS_COMPLETED if len(detection) == 0 else File.STATUS_ATTENTION
        self.model.updateFile(filepath, status=status, analysis=analysis, finishedTime=time.time())


class FileScanWorker(QObject):
    started = Signal(str)
    finished = Signal(str, object)
    error = Signal(str)

    def __init__(self, queue, virustotalApiKey, parent=None):
        super(FileScanWorker, self).__init__(parent)
        self.queue = queue
        self.virustotalApiKey = virustotalApiKey

    async def run(self):
        while True:
            fileInfo = await self.queue.get()
            filepath = fileInfo.get('filepath')
            self.started.emit(filepath)
            with open(filepath, 'rb') as f:
                sha1 = hashlib.sha1(f.read()).hexdigest()
                async with vt.Client(self.virustotalApiKey) as client:
                    analysis = await client.scan_file_async(f)
                    while True:
                        analysis = await client.get_object_async('/analyses/{}', analysis.id)
                        if analysis.status == 'completed':
                            break
                        await asyncio.sleep(10)
                    analysis = await client.get_object_async('/files/{}', sha1)
                    self.queue.task_done()
                    self.finished.emit(filepath, analysis)
