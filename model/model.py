from PySide6.QtCore import QObject

class Model(QObject):
    def __init__(self):
        super().__init__()

    def topMenuPageIdx(self, obj):
        pages = {
            'btn_home': 0,
            'btn_fileScan': 1,
            'btn_folderScan': 2,
            'btn_urlScan' : 3
        }
        btnName = obj.objectName()
        return pages.get(btnName)
