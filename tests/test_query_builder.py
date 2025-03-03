import unittest
from textwrap import dedent
from core import QueryBuilder

class TestQueryBuilder(unittest.TestCase):
    def test_query_builder(self):
        query = QueryBuilder()\
            .SELECT(
                ('t.name', 'threat'),
                ('ft.description', 'file_type')
            )\
            .FROM(('file', 'f'))\
            .LEFT_JOIN('threat t ON t.id = f.threat_id')\
            .WHERE('f.id = ?')

        expected = '''\
        SELECT
            threat AS t.name,
            file_type AS ft.description
        FROM
            f AS file
        LEFT JOIN
            threat t ON t.id = f.threat_id
        WHERE
            f.id = ?
        '''

        self.assertEqual(str(query), dedent(expected))
