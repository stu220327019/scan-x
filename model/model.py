from PySide6.QtCore import QObject

class Model(QObject):
    def __init__(self):
        super().__init__()

    def topMenuPageIdx(self, obj):
        pages = {
            'nav_btn_home': 0,
            'nav_btn_fileScan': 1,
            'nav_btn_dirScan': 2,
            'nav_btn_urlScan' : 3
        }
        btnName = obj.objectName()
        return pages.get(btnName)
