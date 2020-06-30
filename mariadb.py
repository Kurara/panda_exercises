import csv
import mysql.connector
import re


class MariaDBManagement:
    
    """ Global functions
    """
    def connect_db(self, database=None):
        if database:
            self.cnx = mysql.connector.connect(
                user='root',
                password='password',
                host='172.17.0.2',
                database=database
            )
        else:
            self.cnx = mysql.connector.connect(
                user='root',
                password='password',
                host='172.17.0.2'
            )

    def select(self, query):
        _cursor = self.cnx.cursor(buffered=True)
        rows = None
        try:
            _cursor.execute(query)
            rows = _cursor.fetchmany(size=200)
        except Exception as e:
            print("Error executing statement select")
            print(e)
        
        return _cursor.description, rows

    def disconect_db(self):
        self.cnx.close()