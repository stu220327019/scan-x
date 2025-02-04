from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
from view.ui.ui_file_details import Ui_FileDetails

from model import File, Color

class FileDetailsContainer(QWidget):
    def __init__(self, parent=None, fileInfo=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ui = Ui_FileDetails()
        self.ui.setupUi(self)
        self.updateFileInfo(fileInfo)
        self.updateFileScanResult(fileInfo)

    def updateFileInfo(self, fileInfo: dict):
        for label, key in [['Filename', 'filename'], ['Path', 'path'], ['MD5', 'md5'], ['SHA1', 'sha1'],
                           ['SHA256', 'sha256'], ['Size', 'size'], ['Type', 'type']]:
            item = QTreeWidgetItem(self.ui.tbl_fileInfo)
            item.setText(0, label)
            value = '{} Bytes'.format(fileInfo.get(key)) if key == 'size' else fileInfo.get(key)
            item.setText(1, value)
        # self.ui.groupBox_fileInfo.show()

    def updateFileScanResult(self, fileInfo: dict):
        status, analysis = fileInfo.get('status'), fileInfo.get('analysis')
        if analysis:
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
            statusTxt, color = ('No virus detected', Color.SUCCESS) if len(detection) == 0 else ('Virus detected', Color.DANGER)
            self.ui.label_fileScanStatus.setText(statusTxt)
            self.ui.label_fileScanStatus.setStyleSheet('color: {}'.format(color))
            self.ui.label_fileScanElapsedTime.setText('{:.6f} seconds'.format(fileInfo.get('finishedTime') - fileInfo.get('startedTime')))
        else:
            statusTxt, color = (status, Color.SUCCESS) if status != File.STATUS_FAILED else ('Failed', Color.DANGER)
            self.ui.label_fileScanStatus.setText(statusTxt)
            self.ui.label_fileScanStatus.setStyleSheet('color: {}'.format(color))
