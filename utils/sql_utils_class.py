from psycopg2 import OperationalError, connect
from psycopg2.errors import DuplicateDatabase
import re

from psycopg2.extras import RealDictCursor


class SqlUtils:
    USER = "postgres"
    HOST = "localhost"
    PASSWORD = "coderslab"

    @classmethod
    def create_db(cls, db):
        """
        Create db with given name.

        :param str db: name of db
        """
        # Tu umieść rozwiązanie zadania pierwszego.
        try:
            conn = cls._createConnection(None)
            sql = f'Create database {db}'
            crs = conn.cursor()
            crs.execute(sql)

            crs.close()
            conn.close()

        except OperationalError:
            print('Connection error')
        except DuplicateDatabase:
            print('Database already exist')

    @classmethod
    def execute_sql(cls, db, sql_code, sql_params=()):
        """
        Run given sql code with psycopg2.


        :param str db: name of db,
        :param str sql_code: sql code to run
        :param str sql_params: sql params for sql_code


        :rtype: list
        :return: data from psycobg2 cursor as a list (can be None) if nothing to fetch.
        """
        # Tu umieść rozwiązanie zadania drugiego.
        try:
            selectQuery = False
            reResult = re.search(r'select', sql_code, re.I)

            if reResult:
                selectQuery = True

            conn = cls._createConnection(db)

            if selectQuery:
                crs = conn.cursor(cursor_factory=RealDictCursor)
            else:
                crs = conn.cursor()

            crs.execute(sql_code, sql_params)

            if selectQuery:
                resultTmp = crs.fetchall()
                result = cls._fromRealDic2ListDic(resultTmp)
            else:
                result = None

            crs.close()
            conn.close()

            return result

        except OperationalError:
            print('Connection error')

    @classmethod
    def execute_insert_sql(cls, db, sql_code, sql_params=()):
        """
        Run id of inserted element

        :param str db: name of db,
        :param str sql_code: sql code to run
        :param str sql_params: sql params for sql_code

        :rtype: list
        :return: data from psycobg2 cursor as a list (can be None) if nothing to fetch.
        """
        # Tu umieść rozwiązanie zadania drugiego.
        try:
            conn = cls._createConnection(db)
            crs = conn.cursor()

            sql_code += ' RETURNING id'

            crs.execute(sql_code, sql_params)

            result = crs.fetchone()[0]

            crs.close()
            conn.close()

            return result

        except OperationalError:
            print('Connection error')


    @classmethod
    def insert_data(cls,db, table, data):

        sql = f"Insert into {table} Values {data} "
        print(sql)
        try:
            conn = cls._createConnection(db)
            crs = conn.cursor()
            crs.execute(sql)
            crs.close()
            conn.close()
        except OperationalError:
            print('Connection error')



    @classmethod
    def _createConnection(cls, db, autocommit=True):
        if db:
            conn = connect(
                user=cls.USER,
                password=cls.PASSWORD,
                host=cls.HOST,
                database=db
            )
        else:
            conn = connect(
                user=cls.USER,
                password=cls.PASSWORD,
                host=cls.HOST
            )
        conn.autocommit = autocommit
        return conn

    @staticmethod
    def _fromRealDic2ListDic(data):
        result = []
        for row in data:
            rowData = {}
            for column in row:
                rowData[column] = row[column]
            result.append(rowData)
        return result