from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
from PySide6.QtGui import Qt, QIcon
import re
import vt
import time
from qasync import asyncSlot
import asyncio
import json
from pprint import pprint

from view.ui.ui_main import Ui_MainWindow
from .base import Base
from core.config import VIRUS_TOTAL_API_KEY
from lib.entity import URL, URLScanResult, UrlHttpResponse, Analysis, Color

URL_PATTERN = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class URLScan(Base):
    def __init__(self, ui: Ui_MainWindow, *args, **kwargs):
        self.ui = ui
        super().__init__(*args, **kwargs)

    def connectSlotsAndSignals(self):
        self.ui.input_url.textChanged.connect(self.validateURLInput)
        self.ui.btn_urlScan.clicked.connect(self.startURLScan)

    def validateURLInput(self):
        txt = self.ui.input_url.text()
        self.ui.btn_urlScan.setEnabled(re.search(URL_PATTERN, txt) is not None)

    @asyncSlot()
    async def startURLScan(self):
        self.ui.btn_urlScan.setEnabled(False)
        self.ui.btn_urlScan.setText('Scanning...')
        self.ui.input_url.setEnabled(False)
        self.ui.tbl_urlDetails.clear()
        self.ui.tbl_urlScanResult.clear()
        self.ui.label_urlScanElapsedTime.clear()
        self.ui.label_urlScanStatus.clear()
        self.ui.label_urlScanDetection.clear()
        self.startedTime = time.time()
        self.urlScanTask = URLScanTask(self.ui.input_url.text())
        self.urlScanTask.finished.connect(self.updateURLScanResult)
        self.urlScanTask.error.connect(self.scanError)
        await self.urlScanTask.run()

    def resetUi(self):
        self.ui.btn_urlScan.setEnabled(True)
        self.ui.btn_urlScan.setText('Scan')
        self.ui.input_url.setEnabled(True)

    def updateURLScanResult(self, scanResult: URLScanResult):
        item = QTreeWidgetItem(self.ui.tbl_urlDetails)
        item.setText(0, 'URL')
        item.setText(1, scanResult.url.url)
        httpResponse = scanResult.url.httpResponse
        for (label, field) in [('Status Code', 'statusCode'),
                               ('Title', 'title'),
                               ('Content Length', 'contentLength'),
                               ('Content SHA256', 'contentSha256'),
                               ('HTTP Headers', 'headers')]:
            val = httpResponse.get(field)
            if val is None:
                continue
            item = QTreeWidgetItem(self.ui.tbl_urlDetails)
            item.setText(0, label)
            if type(val) in (str, int):
                item.setText(1, f'{val}')
            else:
                for (k, v) in val.items():
                    childItem = QTreeWidgetItem()
                    childItem.setText(0, k)
                    childItem.setText(1, f'{v}')
                    item.addChild(childItem)
                    item.setExpanded(True)
        finishedTime = time.time()
        results = scanResult.analysis.results.values()
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
        statusTxt, color = ('Safe', Color.SUCCESS) if len(detection) == 0 else ('Unsafe', Color.DANGER)
        self.ui.label_urlScanStatus.setText(statusTxt)
        self.ui.label_urlScanStatus.setStyleSheet('color: {}'.format(color))
        self.ui.label_urlScanElapsedTime.setText('{:.6f} seconds'.format(finishedTime - self.startedTime))
        self.resetUi()

    def scanError(self, error):
        print(f'Error: {error}')
        self.resetUi()


class URLScanTask(QObject):
    finished = Signal(object)
    error = Signal(object)

    def __init__(self, url, parent=None):
        super(URLScanTask, self).__init__(parent)
        self.url = url

    def _createScanResult(self, analysis):
        return URLScanResult({
            'url': URL({
                'url': analysis.url,
                'httpResponse': UrlHttpResponse({
                    'statusCode': analysis.get('last_http_response_code'),
                    'contentLength': analysis.get('last_http_response_content_length'),
                    'contentSha256': analysis.get('last_http_response_content_sha256'),
                    'headers': analysis.get('last_http_response_headers'),
                    'title': analysis.get('title')
                })
            }),
            'analysis': Analysis({
                'stats': analysis.last_analysis_stats,
                'results': analysis.last_analysis_results
            }),
            'status': URLScanResult.STATUS_COMPLETED
        })

    async def run(self):
        urlId = vt.url_id(self.url)
        async with vt.Client(VIRUS_TOTAL_API_KEY) as client:
            try:
                try:
                    analysis = await client.get_object_async('/urls/{}', urlId)
                    self.finished.emit(self._createScanResult(analysis))
                except vt.APIError as e:
                    if e.code == 'NotFoundError':
                        analysis = await client.scan_url_async(self.url, wait_for_completion=True)
                        analysis = await client.get_object_async('/urls/{}', urlId)
                        self.finished.emit(self._createScanResult(analysis))
                    else:
                        raise e
            except Exception as e:
                self.error.emit(e)
