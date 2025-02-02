from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from view.ui.ui_file_details import Ui_FileDetails

class FileDetailsContainer(QWidget):
    def __init__(self, parent=None, fileInfo=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ui = Ui_FileDetails()
        self.ui.setupUi(self)
        self.updateFileInfo(fileInfo)

    def updateFileInfo(self, fileInfo: dict):
        for label, key in [['Filename', 'filename'], ['Path', 'path'], ['MD5', 'md5'], ['SHA1', 'sha1'],
                           ['SHA256', 'sha256'], ['Size', 'size'], ['Type', 'type']]:
            item = QTreeWidgetItem(self.ui.tbl_fileInfo)
            item.setText(0, label)
            value = '{} Bytes'.format(fileInfo.get(key)) if key == 'size' else fileInfo.get(key)
            item.setText(1, value)
        # self.ui.groupBox_fileInfo.show()
