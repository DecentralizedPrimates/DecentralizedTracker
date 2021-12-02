from client.singleton_meta_class import SingletonMetaClass
import sqlite3

class DBConnector(metaclass=SingletonMetaClass):
    _instance = None
    _db_connection = None
    _cursor = None

    
    def __init__(self):
        if not self._db_connection:
            self._db_connection = sqlite3.connect(
                'storage/db.sqlite3',
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            self._cursor = self._db_connection.cursor()
    

    def execute(self, query_string, add_param = None):
        if add_param:
            self._cursor.execute(query_string)
        else:
            self._cursor.execute(query_string, add_param)
        
        self._db_connection.commit()

    def fetchone(self, query_string, add_param = None):
        self._cursor.execute(query_string, add_param)
        return self._cursor.fetchone()
