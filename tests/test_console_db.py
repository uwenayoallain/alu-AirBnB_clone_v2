#!/usr/bin/python3
"""DB tests for console create using MySQLdb and skipIf"""
import os
import unittest
from io import StringIO
from unittest.mock import patch


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "DB storage required for this test")
class TestConsoleDBCreate(unittest.TestCase):
    def _count_rows(self, table):
        import MySQLdb
        conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB'),
            port=3306,
            charset='utf8')
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM {}'.format(table))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count

    def test_create_state_increases_row_count(self):
        from console import HBNBCommand
        before = self._count_rows('states')
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="California"')
        after = self._count_rows('states')
        self.assertEqual(after, before + 1)


