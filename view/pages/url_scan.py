from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
from PySide6.QtGui import Qt, QIcon
import re
import vt
import time
from qasync import asyncSlot
import asyncio
import json
from ..ui.ui_main import Ui_MainWindow
from core.config import VIRUS_TOTAL_API_KEY


URL_PATTERN = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class URLScan(QObject):
    def __init__(self, ui: Ui_MainWindow, *args, **kwargs):
        super().__init__()
        self.ui = ui
        self.connect_slots_and_signals()

    def connect_slots_and_signals(self):
        self.ui.input_url.textChanged.connect(self.validateURLInput)
        self.ui.btn_UrlScan.clicked.connect(self.startURLScan)

    def validateURLInput(self):
        txt = self.ui.input_url.text()
        self.ui.btn_UrlScan.setEnabled(re.search(URL_PATTERN, txt) is not None)

    @asyncSlot()
    async def startURLScan(self):
        self.ui.btn_UrlScan.setEnabled(False)
        self.ui.tbl_urlScanResult.clear()
        self.startTime = time.time()
        self.urlScanTask = URLScanTask(self.ui.input_url.text())
        self.urlScanTask.okSignal.connect(self.updateURLScanResult)
        # self.fileScanTask.progressSignal.connect(self.progressFileScanResult)
        await self.urlScanTask.run()

    def updateURLScanResult(self, analysis):
        # self.ui.progressBar.hide()
        results = analysis.last_analysis_results.values()
        detection = [x for x in results if x['result'] not in ('clean', 'unrated')]
        for result in results:
            item = QTreeWidgetItem(self.ui.tbl_urlScanResult)
            item.setText(0, result['engine_name'])
            value = result['result']
            detected = value not in ('clean', 'unrated')
            item.setText(1, value.title())
            icon = QIcon(':/resources/images/icons/exclaimation-circle.svg' if detected else ':/resources/images/icons/check-circle.svg')
            item.setIcon(1, icon)
        self.ui.label_urlScanDetection.setText('{} / {}'.format(len(detection), len(results)))
        statusTxt, color = ('Safe', '#00ff00') if len(detection) == 0 else ('Malicious', '#ff0000')
        self.ui.label_urlScanStatus.setText(statusTxt)
        self.ui.label_urlScanStatus.setStyleSheet('color: {}'.format(color))
        self.ui.label_urlScanElapsedTime.setText('{} seconds'.format(time.time() - self.startTime))
        # self.ui.groupBox_fileScanResult.show()


class URLScanTask(QObject):
    okSignal = Signal(object)
    progressSignal = Signal()

    def __init__(self, url, parent=None):
        super(URLScanTask, self).__init__(parent)
        self.url = url

    async def run(self):
        url_id = vt.url_id(self.url)
        async with vt.Client(VIRUS_TOTAL_API_KEY) as client:
            analysis = await client.scan_url_async(self.url)
            while True:
                analysis = await client.get_object_async('/analyses/{}', analysis.id)
                if analysis.status == 'completed':
                    break
                self.progressSignal.emit()
                await asyncio.sleep(30)
            result = await client.get_object_async('/urls/{}', url_id)
            # print(json.dumps(result, indent=4, default=vars))
            self.okSignal.emit(result)
