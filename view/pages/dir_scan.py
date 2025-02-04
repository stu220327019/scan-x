from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
from PySide6.QtGui import Qt, QIcon
import os
import hashlib
import vt
import json
import time
import asyncio
import magic
from qasync import asyncSlot
from ..ui.ui_main import Ui_MainWindow
from core.config import VIRUS_TOTAL_API_KEY

def get_dir_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        dir_content = []
        for dir in dirs:
            go_inside = os.path.join(startpath, dir)
            dir_content.append(get_dir_tree(go_inside))
        files_lst = []
        for f in files:
            files_lst.append(f)
        return {'name': root, 'files': files_lst, 'dirs': dir_content}


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


class DirScan(QObject):
    def __init__(self, ui: Ui_MainWindow, *args, **kwargs):
        super().__init__()
        self.ui = ui
        self.ui.groupBox_dirScan.hide()
        self.connect_slots_and_signals()

    def connect_slots_and_signals(self):
        self.ui.btn_dirBrowse.clicked.connect(self.dirBrowse)
        # self.ui.btn_fileScan.clicked.connect(self.startFileScan)

    def dirBrowse(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            self.dir = dlg.selectedFiles()[0]
            self.ui.lbl_dirSelected.setText(self.dir)
            self.ui.lbl_dirSelected.setStyleSheet("color: #0000ff")
            self.ui.btn_dirScan.setEnabled(True)
            self.ui.groupBox_dirScan.show()
            self.ui.groupBox_dirScan.setTitle('Directory - {}'.format(self.dir))

            self.ui.tree_dirScan.clear()

            dir_tree = get_dir_tree(self.dir)
            dir_tree_items = build_tree_widget_items(dir_tree)
            self.ui.tree_dirScan.insertTopLevelItems(0, dir_tree_items)

    def updateFileInfo(self, fileInfo: dict):
        for label, key in [['Name', 'name'], ['Path', 'path'], ['MD5', 'md5'], ['SHA1', 'sha1'],
                           ['SHA256', 'sha256'], ['Size', 'size'], ['Type', 'type']]:
            item = QTreeWidgetItem(self.ui.tbl_fileInfo)
            item.setText(0, label)
            value = '{} Bytes'.format(fileInfo.get(key)) if key == 'size' else fileInfo.get(key)
            item.setText(1, value)
        self.ui.groupBox_fileInfo.show()

    @asyncSlot()
    async def startFileScan(self):
        self.ui.btn_fileScan.setEnabled(False)
        self.ui.progressBar.show()
        self.ui.progressBar.setValue(10)
        self.ui.tbl_fileScanResult.clear()
        self.startTime = time.time()
        self.fileScanTask = FileScanTask(self.filepath)
        self.fileScanTask.okSignal.connect(self.updateFileScanResult)
        self.fileScanTask.progressSignal.connect(self.progressFileScanResult)
        await self.fileScanTask.run()

    def progressFileScanResult(self):
        self.ui.progressBar.setValue(self.ui.progressBar.value() + 5)

    def updateFileScanResult(self, analysis):
        self.ui.progressBar.hide()
        results = analysis.last_analysis_results.values()
        detection = [x for x in results if x['result'] is not None]
        for result in results:
            item = QTreeWidgetItem(self.ui.tbl_fileScanResult)
            item.setText(0, result['engine_name'])
            detected = result['result'] is not None
            value = result['result'] if detected else 'Undetected'
            item.setText(1, value)
            icon = QIcon(':/resources/images/icons/exclaimation-circle.svg' if detected else ':/resources/images/icons/check-circle.svg')
            item.setIcon(1, icon)
        self.ui.label_fileScanDetection.setText('{} / {}'.format(len(detection), len(results)))
        statusTxt, color = ('No virus detected', '#00ff00') if len(detection) == 0 else ('Virus detected', '#ff0000')
        self.ui.label_fileScanStatus.setText(statusTxt)
        self.ui.label_fileScanStatus.setStyleSheet('color: {}'.format(color))
        self.ui.label_fileScanElapsedTime.setText('{} seconds'.format(time.time() - self.startTime))
        self.ui.groupBox_fileScanResult.show()


class FileDetailsThread(QThread):
    okSignal = Signal(dict)

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
        self.okSignal.emit(fileDetails)


class FileScanTask(QObject):
    okSignal = Signal(object)
    progressSignal = Signal()

    def __init__(self, filepath, parent=None):
        super(FileScanTask, self).__init__(parent)
        self.filepath = str(filepath)

    async def run(self):
        with open(self.filepath, 'rb') as f:
            sha1 = hashlib.sha1(f.read()).hexdigest()
            # sha1 = '9f101483662fc071b7c10f81c64bb34491ca4a877191d464ff46fd94c7247115'
            async with vt.Client(VIRUS_TOTAL_API_KEY) as client:
                analysis = await client.scan_file_async(f)
                while True:
                    analysis = await client.get_object_async('/analyses/{}', analysis.id)
                    if analysis.status == 'completed':
                        break
                    self.progressSignal.emit()
                    await asyncio.sleep(30)
                result = await client.get_object_async('/files/{}', sha1)
                # print(json.dumps(result, indent=4, default=vars))
                self.okSignal.emit(result)
