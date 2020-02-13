from .connect import Connect

class GenericConnect(Connect):
    def __init__(self, DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE, CHARSET):
        super().__init__()
        self._DB_USER = DB_USER
        self._DB_PASS = DB_PASS
        self._DB_HOST = DB_HOST
        self._DB_PORT = DB_PORT
        self._DATABASE = DATABASE
        self._CHARSET = CHARSET

    def getTableDataFrame(self, tablename=''):
        queryGet = 'SELECT * FROM {}'.format(tablename)
        return self.readDataFrame(queryGet)

    def getQueryDataFrame(self, query=''):
        return self.readDataFrame(query)