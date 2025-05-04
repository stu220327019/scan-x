from view import View
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase,QIcon
import sys
import asyncio
import os
from qasync import QEventLoop
from core import config, DB, Router

def initDB(db: DB):
    with open('res/create_tables.sql', 'r') as f:
        cur = db.conn.cursor()
        cur.executescript(f.read())
        cur.execute('PRAGMA foreign_keys = ON')

def main():
    # os.putenv('QT_QPA_PLATFORM','windows:darkmode=0')
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    db = DB(config.DB_FILE)
    initDB(db)

    ctx = {
        'db': db,
        'router': Router()
    }

    view = View(ctx)
    view.show()

    # sys.exit(app.exec())
    with loop:
        loop.run_forever()


if __name__ == '__main__':
    main()
