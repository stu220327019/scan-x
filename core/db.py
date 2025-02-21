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


class QueryBuilder:
    EQUAL = 0
    NOT_EQUAL = 1
    LIKE = 2

    JOIN = 0

    def __init__(self):
        self._whereClauses = []
        self._joinClauses = []

    def where(self, field, val, cond=EQUAL):
        self._whereClauses.append((field, val, cond))
        return self

    def join(self, tbl, a, b, joinType=JOIN):
        self._joinClauses.append((tbl, a, b, joinType))
        return self

    def build(self):
        where = ''
        if len(self._whereClauses) > 0:
            strWhereClauses = []
            for (field, val, cond) in self._whereClauses:
                op = ['=', '!=', 'LIKE'][cond]
                if type(val) == str:
                    val = val.replace('\'', '\'\'')
                    if cond == self.LIKE:
                        val = f'%{val}%'
                    val = f'\'{val}\''
                strWhereClauses.append(f'{field} {op} {val}')
            where = 'AND ' + ' AND '.join(strWhereClauses)

        join = ''
        if len(self._joinClauses) > 0:
            strJoinClauses = [f' {tbl} ON {a} = {b}'
                              for (tbl, a, b, _) in self._joinClauses]
            join = 'JOIN ' + ' JOIN '.join(strJoinClauses)

        return {
            'where': where,
            'join': join
        }
