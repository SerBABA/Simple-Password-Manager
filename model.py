import sqlite3
import account
import user


class Model:

    def __init__(self, db_name):
        self.DB_NAME = db_name
        self.STORED_ACCOUNTS_TABLE_NAME = "accounts"
        self.USERS_TABLE_NAME = "users"
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
    
    def create_tables(self):
        # Creating encrypted accounts table for database
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER NOT NULL AUTOINCREMENT,
            user INTEGER NOT NULL,
            type TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            UNIQUE (id, user),
            FOREIGN KEY (user) REFERENCES {} (id)
            )""".format(self.STORED_ACCOUNTS_TABLE_NAME, self.USERS_TABLE_NAME))

            # Creating users table
            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER AUTOINCREMENT PRIMARY KEY
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            UNIQUE (username)
            )""".format(self.USERS_TABLE_NAME))

            self.commit()
        except:
            self.rollback()


    def close_conn(self):
        self.conn.close()


    def insert_new_account(self, ):
        """ """


