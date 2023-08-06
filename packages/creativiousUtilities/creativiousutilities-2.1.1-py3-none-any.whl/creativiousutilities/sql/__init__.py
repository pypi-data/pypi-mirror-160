import mysql.connector
from mysql.connector import errorcode
import uuid


class MySQL:
    def __init__(self):
        self.connection : mysql.connector.MySQLConnection = None
        pass
    def connect(self, host: str, user: str, password: str, database: str, port: int = 3306):
        if self.connection is not None:
            try:
                ID = str(uuid.uuid4().int)
                connection = {}
                self.connection : mysql.connector.MySQLConnection = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    raise "Connection to database has failed due to wrong password or username!"
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    raise "Database doesn't exist!"
                else:
                    raise err
            return self.connection
        else:
            return None
    def disconnect(self):
        self.connection.close()
        self.connection = None








