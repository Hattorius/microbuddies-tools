import mysql.connector

class database:
    def __init__(self, host, username, password, database) -> None:
        self.connection = mysql.connector.connect(
            host=host,
            username=username,
            password=password,
            database=database
        )
        pass
    
    def query(self, query) -> any:
        cursor = self.connection.cursor()
        cursor.execute(query)
        if "select" in query.lower():
            return cursor.fetchall()
