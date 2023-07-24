import mysql.connector

class MysqlDB:
    def __init__(self) -> None:
        self.conn = None
        self.database = None
    
    def connection(self, user:str = 'root', password:str = '', host:str = 'localhost', port:str = '3306', database:str = 'despesas'):
        self.conn = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database)
    
    def close(self):
        self.conn.close()
    
    def select(self, query:str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

