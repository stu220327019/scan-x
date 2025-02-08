from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
from view.ui.ui_scan_result import Ui_ScanResult

from lib.entity import URL, Color, UrlScanResult
from lib import utils

class UrlScanResultContainer(QWidget):
    def __init__(self, parent=None, scanResult:UrlScanResult=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ui = Ui_ScanResult()
        self.ui.setupUi(self)
        self.updateUrlDetails(scanResult.url)
        self.updateAnalysisResults(scanResult)

    def updateUrlDetails(self, url: URL):
        self.ui.groupBox_details.setTitle('URL Details')
        item = QTreeWidgetItem(self.ui.tbl_details)
        item.setText(0, 'URL')
        item.setText(1, url.url)
        httpResponse = url.httpResponse
        for (label, field) in [('Status Code', 'statusCode'),
                               ('Title', 'title'),
                               ('Content Length', 'contentLength'),
                               ('Content SHA256', 'contentSha256'),
                               ('HTTP Headers', 'headers')]:
            val = httpResponse.get(field)
            if val is None:
                continue
            item = QTreeWidgetItem(self.ui.tbl_details)
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

    def updateAnalysisResults(self, scanResult: UrlScanResult):
        analysisResults = scanResult.analysis.results
        if not isinstance(analysisResults, list):
                analysisResults = analysisResults.values()
        detection = [x for x in analysisResults if x['result'] not in ('clean', 'unrated')]
        for result in analysisResults:
            item = QTreeWidgetItem(self.ui.tbl_analysisResults)
            item.setText(0, result['engine_name'])
            value = result['result']
            detected = value not in ('clean', 'unrated')
            item.setText(1, value)
            icon = QIcon(':/resources/images/icons/exclaimation-circle.svg' if detected else ':/resources/images/icons/check-circle.svg')
            item.setIcon(1, icon)
        self.ui.label_detection.setText('{} / {}'.format(len(detection), len(analysisResults)))
        statusTxt, color = ('Safe', Color.SUCCESS) if len(detection) == 0 else ('Unsafe', Color.DANGER)
        self.ui.label_status.setText(statusTxt)
        self.ui.label_status.setStyleSheet('color: {}'.format(color))
        self.ui.label_elapsedTime.setText('{:.6f} seconds'.format(scanResult.finishedTime - scanResult.startedTime))
