
# python packages imports
import sqlite3
import re

# lib imports
from lib import Account, User


class DatabaseHandler:

    def __init__(self, db_name='vault'):

        # Database related stuff
        if re.fullmatch(r'[a-zA-Z]+.db', db_name) is None:
            self.DB_NAME = db_name + '.db'
        else:
            self.DB_NAME = db_name
        self.STORED_ACCOUNTS_TABLE_NAME = "Accounts"
        self.USERS_TABLE_NAME = "Users"
        self.conn = sqlite3.connect(self.DB_NAME)
        self.conn.isolation_level = None
        self.c = self.conn.cursor()
        self.create_tables()


    def begin_transaction(self):
        self.conn.execute('begin')

    def commit(self):
        self.conn.execute('commit')


    def rollback(self):
        self.conn.execute('rollback')
 

    def close_conn(self):
        self.conn.close()


    def create_tables(self):
        # Creating encrypted accounts table for database
        self.begin_transaction()
        try:
            # Creating users table
            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            UNIQUE (username)
            );""".format(self.USERS_TABLE_NAME))

            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER NOT NULL,
            type TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            UNIQUE (id, user),
            FOREIGN KEY (user) REFERENCES {} (id)
            );""".format(self.STORED_ACCOUNTS_TABLE_NAME, self.USERS_TABLE_NAME))

            # Creating ensureUserExists trigger. This trigger raises a Unknown User Id when
            # insertion is occured on the SOTRED_ACCOUNTS_TABLE. This also triggers a rollback,
            # which undoes the changes. THis is to prevent addition of accounts that don't link
            # into any other user accounts. 
            self.c.execute("""CREATE TRIGGER IF NOT EXISTS ensureUserExists
            BEFORE INSERT ON {}
            FOR EACH ROW
            WHEN NOT EXISTS (SELECT * FROM {} WHERE id=new.user)
            BEGIN
                SELECT RAISE (FAIL, 'Unknown user id.');
            END;
            """.format(self.STORED_ACCOUNTS_TABLE_NAME, self.USERS_TABLE_NAME))

            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


    def insert_new_account(self, new_account):
        """ """
        if not isinstance(new_account, Account.Account):
            raise TypeError("new_account must be of type Account")
        
        self.begin_transaction()

        try:
            sql = """INSERT INTO {} (user, type, username, password, salt)
                VALUES (?, ?, ?, ?, ?)""".format(self.STORED_ACCOUNTS_TABLE_NAME)

            self.c.execute(sql, (new_account.user, new_account.type, new_account.username,
             new_account.password, new_account.salt))
        
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


    def insert_new_user(self, new_user):
        """ """
        if not isinstance(new_user, User.User):
            raise TypeError("new_user must be of type User")

        self.begin_transaction()
        
        try:
            sql = """INSERT INTO {} (username, password, salt) 
                VALUES (?, ?)""".format(self.USERS_TABLE_NAME)

            self.c.execute(sql, (new_user.username, new_user.password, new_user.salt))

            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


    def delete_account(self, account_id=None, owner_id=None):
        """

        """
        if not isinstance(account_id, int):
            raise TypeError("account_id must of type integer.")
        if not isinstance(owner_id, int):
            raise TypeError("user_id must be of type integer")

            self.begin_transaction()

        try:
            query = """DELETE FROM {} WHERE id = ? AND user = ?""".format(self.STORED_ACCOUNTS_TABLE_NAME)
            self.c.execute(query, (account_id, owner_id))
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


if __name__ == "__main__":
    db = DatabaseHandler("vault")
    ac =  Account.Account("type", "user", "pass", "salt", 1)
    db.insert_new_account(ac)
        

