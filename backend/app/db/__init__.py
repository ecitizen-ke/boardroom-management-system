from flask import current_app as app
import MySQLdb
from utils import statements


class Connection:
    def __init__(self):
        self.host = app.config["MYSQL_HOST"]
        self.user = app.config["MYSQL_USER"]
        self.password = app.config["MYSQL_PASSWORD"]
        self.db = app.config["MYSQL_DB"]

        self.conn = MySQLdb.connect(
            host=self.host, database=self.db, user=self.user, password=self.password
        )
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def create_tables(self):
        for statement in statements.values():
            self.cursor.execute(statement)

    def insert(self, statement, data):
        self.cursor.execute(statement, data)
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def fetchmany(self, statement):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def fetchandfilter(self, statement, data):
        self.cursor.execute(statement, data)
        return self.cursor.fetchall()

    def fetchone(self, statement, data):
        self.cursor.execute(statement, data)
        return self.cursor.fetchone()
