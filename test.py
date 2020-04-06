import unittest
import pymysql

from python import app


class TestCase(unittest.TestCase):
    conn = None
    cur = None
    app = None

    def setUp(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    passwd='root',
                                    db='mydb',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()

        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name, col_name, col_type):
        query = f'CREATE TABLE {table_name} ({col_name} {col_type});'
        self.cur.execute(query)
        self.conn.commit()

        query = 'SHOW Tables;'
        self.cur.execute(query)
        self.conn.commit()
        tables = self.cur.fetchall()
        t = table_name in [list(x.values())[0] for x in tables]
        self.assertTrue(t)

    def drop_table(self, table_name):
        query = f'DROP TABLE {table_name};'
        self.cur.execute(query)
        self.conn.commit()

        query = 'SHOW Tables;'
        self.cur.execute(query)
        self.conn.commit()
        tables = self.cur.fetchall()
        t = table_name not in [list(x.values())[0] for x in tables]
        self.assertTrue(t)

    def test_post_create_db(self):
        db_name = 'my_test_db'

        response = self.app.post('CreateDB', data={'name': db_name})
        self.assertEqual(response.status_code, 302)

        query = 'SHOW DATABASES;'
        self.cur.execute(query)
        self.conn.commit()
        databases = self.cur.fetchall()
        t = db_name in [x['Database'] for x in databases]
        self.assertTrue(t)

        query = f'DROP DATABASE {db_name};'
        self.cur.execute(query)
        self.conn.commit()

    def test_post_delete_db(self):
        db_name = 'my_test_db_for_delete'

        query = f'CREATE DATABASE {db_name};'
        self.cur.execute(query)
        self.conn.commit()

        response = self.app.post('DeleteDB', data={'name': db_name})
        self.assertEqual(response.status_code, 302)

        query = 'SHOW DATABASES;'
        self.cur.execute(query)
        self.conn.commit()
        databases = self.cur.fetchall()

        t = db_name not in [x['Database'] for x in databases]
        self.assertTrue(t)

    def test_post_create_table(self):
        table_name = 'test_table_for_create'
        col_name = 'test_column_for_create'
        col_type = 'VARCHAR(20)'

        response = self.app.post('CreateTB', data={'name': table_name,
                                                   'name_col': col_name,
                                                   'int_col': col_type})
        self.assertEqual(response.status_code, 302)

        query = 'SHOW Tables;'
        self.cur.execute(query)
        self.conn.commit()
        tables = self.cur.fetchall()
        t = table_name in [list(x.values())[0] for x in tables]
        self.assertTrue(t)

        self.drop_table(table_name)

    def test_post_delete_table(self):
        table_name = 'test_table_for_delete'
        col_name = 'test_column'
        col_type = 'VARCHAR(20)'

        self.create_table(table_name, col_name, col_type)

        response = self.app.post('DeleteTB', data={'name': table_name})
        self.assertEqual(response.status_code, 302)

        query = 'SHOW Tables;'
        self.cur.execute(query)
        self.conn.commit()
        tables = self.cur.fetchall()
        t = table_name not in [list(x.values())[0] for x in tables]
        self.assertTrue(t)

    def test_post_add_column(self):
        table_name = 'test_table_for_add_col'
        col_name = 'test_column'
        new_col_name = 'added_test_column'
        col_type = 'VARCHAR(20)'

        self.create_table(table_name, col_name, col_type)

        response = self.app.post('ChangeTB/Add', data={'name': table_name,
                                                       'name_col': new_col_name,
                                                       'int_col': col_type})
        self.assertEqual(response.status_code, 302)

        query = f'SHOW COLUMNS FROM {table_name};'
        self.cur.execute(query)
        self.conn.commit()
        columns = self.cur.fetchall()
        t = new_col_name in [list(x.values())[0] for x in columns]
        self.assertTrue(t)

        self.drop_table(table_name)

    def test_get_create_db(self):
        response = self.app.get('CreateDB')
        self.assertEqual(response.status_code, 200)

    def test_get_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_delete_db(self):
        response = self.app.get('DeleteDB')
        self.assertEqual(response.status_code, 200)

    def test_get_create_tb(self):
        response = self.app.get('CreateTB')
        self.assertEqual(response.status_code, 200)

    def test_get_delete_tb(self):
        response = self.app.get('DeleteTB')
        self.assertEqual(response.status_code, 200)

    def test_get_change_tb_edit(self):
        response = self.app.get('ChangeTB/Edit')
        self.assertEqual(response.status_code, 200)

    def test_get_change_tb_add(self):
        response = self.app.get('ChangeTB/Add')
        self.assertEqual(response.status_code, 200)

    def test_get_select_tb(self):
        response = self.app.get('SelectTB')
        self.assertEqual(response.status_code, 200)

    def test_get_select_tb_select_all(self):
        response = self.app.get('SelectTB/Select_all')
        self.assertEqual(response.status_code, 200)

    def test_get_select_tb_count(self):
        response = self.app.get('SelectTB/count')
        self.assertEqual(response.status_code, 200)
