import unittest
import os
import geoip2.database
import tempfile
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from sqlite_manager import insert_if_not_exist, select, update_value
from utils import country_by_ip
from flask_tests.con_lib import DBConn

reader = geoip2.database.Reader(os.path.join('CountryDB',
                                             'GeoLite2-Country.mmdb'))


class FlaskTest(unittest.TestCase):
    a = tempfile.mkstemp(suffix='.db')
    name = str(a[1].split("\\")[-1])
    database = f'{name}'

    def setUp(self, db=database):
        with DBConn(db) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE counter (
                            "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                            "count"	INTEGER DEFAULT 0)""")
            pages = [(1, 2),
                     (2, 3),
                     (3, 4),
                     (5, 6),
                     (6, 7)]
            cursor.executemany("INSERT INTO counter VALUES (?,?)", pages)
            cursor.fetchall()
            conn.commit()

    def test_select(self, db=database):
        self.assertEqual(2, select(db, 'counter',
                                   'count', id=1)[0][0])

    def test_update_value(self, db=database):
        update_value(db, 'counter', ('count', 3), id=1)
        self.assertEqual(select(db, 'counter',
                                'count', id=1)[0][0], 3)

    def test_insert_if_not_exist(self, db=database):
        insert_if_not_exist(db, 'counter', id=8, count=9)
        self.assertEqual(select(db, 'counter',
                                'count', id=8)[0][0], 9)

    def test_country_by_ip(self):
        russian_ip = '5.19.255.255'
        country = country_by_ip(russian_ip, reader)
        self.assertEqual('Russia', country)

    def tearDown(self, db=database):
        os.remove(db)


if __name__ == '__main__':
    unittest.main()
