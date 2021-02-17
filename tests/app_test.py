import os
import sys
import unittest
import shutil
import sqlite3

_CWD = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(_CWD)

import app_utils

CWD = app_utils.CWD

conn = sqlite3.connect('test.db')

create_query = '''create temp table records(
                id INT,
                first_name VARCHAR,
                last_name VARCHAR,
                street_address VARCHAR,
                state VARCHAR,
                zip INT,
                change_in_purchase_status VARCHAR,
                product_id INT,
                product_name VARCHAR,
                product_purchase_amount INT,
                timestamp DATETIME
            )

          '''

class TestUploadFiles(unittest.TestCase):
    def setUp(self):
        os.chdir(CWD)
        shutil.copyfile('tests/ZKWDLhxw.txt', 'uploads/ZKWDLhxw.txt')
        app_utils.DATABASE = os.path.join(CWD, 'test.db')
        self.engine = app_utils.get_engine()
        with self.engine.connect() as conn:
            conn.execute(create_query)

    def tearDown(self):
        os.chdir(_CWD)
        os.remove('uploads/ZKWDLhxw.txt')
        self.engine.dispose()

    def test_get_uploaded_files(self):
        self.assertEqual(app_utils.get_uploaded_files(), ['ZKWDLhxw.txt'])

    def test_read_file(self):
        self.assertEqual(app_utils.read_file('ZKWDLhxw.txt').shape, (5,11))

    def test_upload_file(self):
        df = app_utils.read_file('ZKWDLhxw.txt')
        with self.engine.connect() as conn:
            check = conn.execute('select * from records').fetchall()
            self.assertEqual(len(check), 5)
            self.assertEqual(len(check[0]), 11)



if __name__ == '__main__':
    unittest.main()