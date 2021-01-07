import mysql.connector
import pandas as pd
from sqlalchemy import create_engine, Integer

class Connect():
    def __init__(self):
        super().__init__()
        self._DB_USER = 'root'
        self._DB_PASS = ''
        self._DB_HOST = 'localhost'
        self._DB_PORT = 3306
        self._DATABASE = 'test'
        self._CHARSET='utf8mb4'

    def inputToDataBase(self, queryInput, queryGet, areMany = False):
        connection = mysql.connector.connect(host=self._DB_HOST, user=self._DB_USER, password=self._DB_PASS, db=self._DATABASE, charset=self._CHARSET)
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryInput)
                connection.commit()
            with connection.cursor() as cursor:
                cursor.execute(queryGet)
                if areMany:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
        except:
            result = None
            connection.rollback()
        finally:
            connection.close()
        return result

    def outputFromDataBase(self, queryGet, areMany = False):
        connection = mysql.connector.connect(host=self._DB_HOST, user=self._DB_USER, password=self._DB_PASS, db=self._DATABASE, charset=self._CHARSET)
        try:
            with connection.cursor() as cursor:
                cursor.execute(queryGet)
                if areMany:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
        except:
            result = None
            connection.rollback()
        finally:
            connection.close()
        return result

    def readDataFrame(self, queryGet):
        try:
            connect_string = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset={}'.format(self._DB_USER, self._DB_PASS, self._DB_HOST, self._DB_PORT, self._DATABASE, self._CHARSET)
            engine = create_engine(connect_string)
            df = pd.read_sql_query(queryGet, engine)
        except:
            df = pd.DataFrame
        return df