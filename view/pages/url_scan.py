from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem
from PySide6.QtGui import Qt, QIcon
import re
import vt
import time
from qasync import asyncSlot
import asyncio
import json
import sqlite3

from view.ui.ui_main import Ui_MainWindow
from .base import Base
from core.config import VIRUS_TOTAL_API_KEY
from lib.entity import URL, UrlScanResult, UrlHttpResponse, Analysis, Color

URL_PATTERN = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class URLScan(Base):
    def __init__(self, ui: Ui_MainWindow, ctx=None, *args, **kwargs):
        self.ui = ui
        self.db: DB = ctx.get('db')
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

    def updateURLScanResult(self, scanResult: UrlScanResult):
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
        analysisResults = scanResult.analysis.results.values()
        detection = [x for x in analysisResults if x['result'] not in ('clean', 'unrated')]
        for result in analysisResults:
            item = QTreeWidgetItem(self.ui.tbl_urlScanResult)
            item.setText(0, result['engine_name'])
            value = result['result']
            detected = value not in ('clean', 'unrated')
            item.setText(1, value.title())
            icon = QIcon(':/resources/images/icons/exclaimation-circle.svg' if detected else ':/resources/images/icons/check-circle.svg')
            item.setIcon(1, icon)
        self.ui.label_urlScanDetection.setText('{} / {}'.format(len(detection), len(analysisResults)))
        statusTxt, color = ('Safe', Color.SUCCESS) if len(detection) == 0 else ('Unsafe', Color.DANGER)
        self.ui.label_urlScanStatus.setText(statusTxt)
        self.ui.label_urlScanStatus.setStyleSheet('color: {}'.format(color))
        self.ui.label_urlScanElapsedTime.setText('{:.6f} seconds'.format(finishedTime - self.startedTime))
        self.resetUi()
        try:
            self.db.beginTransaction()
            url = scanResult.url
            urlId = self.db.fetchOneCol('SELECT id FROM url WHERE url = ?', [url.url])
            if not urlId:
                cur = self.db.exec('INSERT INTO url (url, created_at) VALUES (?, ?)', [url.url, time.time()])
                urlId = cur.lastrowid
            httpResponse = url.httpResponse
            if not self.db.fetchOneCol('SELECT id FROM url_http_response WHERE url_id = ? AND content_sha256 = ?',
                                       [urlId, httpResponse.get('contentSha256')]):
                self.db.exec("""
                INSERT INTO url_http_response (url_id, status_code, content_length, content_sha256, title, headers, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                             [urlId,
                              httpResponse.get('statusCode'),
                              httpResponse.get('contentLength'),
                              httpResponse.get('contentSha256'),
                              httpResponse.get('title'),
                              json.dumps(dict(httpResponse.get('headers'))) if httpResponse.get('headers') else None,
                              time.time()])
            cur = self.db.exec("""
            INSERT INTO url_scan_result (url_id, analysis_stats, analysis_results, clean, started_at, finished_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                         [urlId,
                          json.dumps(dict(scanResult.analysis.stats)),
                          json.dumps([dict(res) for res in analysisResults]),
                          len(detection) == 0, self.startedTime, finishedTime, time.time()])
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
                INSERT INTO analysis (engine_id, virus_id, category, type, url_scan_result_id)
                VALUES (?, ?, ?, ?, ?)
                """, [engineId, virusId, analysisResult.get('category'), 'url', scanResultId])
            self.db.commit()
        except sqlite3.Error as e:
            print(f"DB error: {e}")
            self.db.rollback()

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
        return UrlScanResult({
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
            'status': UrlScanResult.STATUS_COMPLETED
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
