from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
from view.ui.ui_scan_result import Ui_ScanResult

from lib.entity import File, Color, FileScanResult
from lib import utils

class FileScanResultContainer(QWidget):
    def __init__(self, parent=None, scanResult:FileScanResult=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ui = Ui_ScanResult()
        self.ui.setupUi(self)
        self.updateFileDetails(scanResult.file)
        self.updateAnalysisResults(scanResult)

    def updateFileDetails(self, fileInfo: File):
        self.ui.groupBox_details.setTitle('File Details')
        for label, key in [['Filename', 'filename'], ['Path', 'path'], ['MD5', 'md5'], ['SHA1', 'sha1'],
                           ['SHA256', 'sha256'], ['Size', 'size'], ['Type', 'type']]:
            item = QTreeWidgetItem(self.ui.tbl_details)
            item.setText(0, label)
            value = '{} ({} Bytes)'.format(utils.sizeof_fmt(fileInfo.get(key)), fileInfo.get(key)) \
                if key == 'size' else fileInfo.get(key)
            item.setText(1, value)

    def updateAnalysisResults(self, scanResult: FileScanResult):
        status = scanResult.status
        if scanResult.analysis:
            analysisResults = scanResult.analysis.results
            if not isinstance(analysisResults, list):
                analysisResults = analysisResults.values()
            detection = [x for x in analysisResults if x['result'] is not None]
            for result in analysisResults:
                item = QTreeWidgetItem(self.ui.tbl_analysisResults)
                item.setText(0, result['engine_name'])
                detected = result['result'] is not None
                value = result['result'] if detected else 'Undetected'
                item.setText(1, value)
                icon = QIcon(':/resources/images/icons/exclaimation-circle.svg' if detected else ':/resources/images/icons/check-circle.svg')
                item.setIcon(1, icon)
            self.ui.label_detection.setText('{} / {}'.format(len(detection), len(analysisResults)))
            statusTxt, color = ('No virus detected', Color.SUCCESS) if len(detection) == 0 else ('Virus detected', Color.DANGER)
            self.ui.label_status.setText(statusTxt)
            self.ui.label_status.setStyleSheet('color: {}'.format(color))
            self.ui.label_elapsedTime.setText('{:.6f} seconds'.format(scanResult.finishedTime - scanResult.startedTime))
        else:
            statusTxt, color = (status, Color.INFO) if status != FileScanResult.STATUS_FAILED else ('Failed', Color.DANGER)
            self.ui.label_status.setText(statusTxt)
            self.ui.label_status.setStyleSheet('color: {}'.format(color))
