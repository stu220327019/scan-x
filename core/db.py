import sqlite3
from sqlite3 import Error

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DB:
    conn: sqlite3.Connection = None

    def __init__(self, dbFile):
        self.createConnection(dbFile)

    def createConnection(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = dict_factory

    def exec(self, sql, params=(), commit=False):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        if commit:
            self.commit()
        return cur

    def fetchOne(self, sql, params=()):
        cur = self.exec(sql, params)
        return cur.fetchone()

    def fetchOneCol(self, sql, params=()):
        res = self.fetchOne(sql, params)
        if res:
            return next(iter(res.values()))

    def fetchAll(self, sql, params=()):
        cur = self.exec(sql, params)
        return cur.fetchall()

    def fetch(self, size, sql, params=()):
        cur = self.exec(sql, params)
        return cur.fetchmany(size)

    def beginTransaction(self):
        self.exec('BEGIN')

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
        # self.exec('rollback')
