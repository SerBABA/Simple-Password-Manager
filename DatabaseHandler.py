
# python packages imports
import sqlite3
import re

# lib imports
from lib import Account, User


def TransactionDecorator(func):
    def wrapper(obj, *args, **kwargs):
        obj.begin_transaction()
        try:
            res =  func(obj, *args, **kwargs)
            obj.commit()
            return res
        except sqlite3.Error as e:
            print(e)
            obj.rollback()
            return None
    return wrapper


# New idea requires the db (database) to have a seperate file per user, and when a user wants
# to access their data the db is loaded into memory and read for the user.
class DatabaseHandler:

    def __init__(self, db_name='vault'):

        # Database related stuff
        if re.fullmatch(r'[a-zA-Z]+.db', db_name) is None:
            self.db_name = db_name + '.db'
        else:
            self.db_name = db_name
        self.STORED_ACCOUNTS_TABLE_NAME = "Accounts"
        self.USERS_TABLE_NAME = "Users"
        self.conn = sqlite3.connect(self.db_name)
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
            hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            UNIQUE (username)
            );""".format(self.USERS_TABLE_NAME))

            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER NOT NULL,
            type TEXT NOT NULL,
            username TEXT NOT NULL,
            hash TEXT NOT NULL,
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
            sql = """INSERT INTO {} (user, type, username, hash, salt)
                VALUES (?, ?, ?, ?, ?)""".format(self.STORED_ACCOUNTS_TABLE_NAME)

            self.c.execute(sql, (new_account.user, new_account.type, new_account.username,
             new_account.password, new_account.salt))
        
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


    def disconnect(self):
        """ """
        self.c.close()


    def insert_new_user(self, new_user):
        """ """
        if not isinstance(new_user, User.User):
            raise TypeError("new_user must be of type User")

        self.begin_transaction()
        
        try:
            sql = """INSERT INTO {} (username, hash, salt) 
                VALUES (?, ?, ?)""".format(self.USERS_TABLE_NAME)

            self.c.execute(sql, (new_user.username, new_user.password, new_user.salt))

            self.commit()
            return {'status': 200, 'msg': 'User successfully created.'}
        except Exception as e:
            print(e)
            self.rollback()
            return {'status': 500, 'msg': 'Something went wrong while adding user.'}

    @TransactionDecorator
    def get_user_creds(self, username):
        """ """
        if not isinstance(username, str):
            raise TypeError('Username must be of type string!')
        
        # self.begin_transaction()

        try:
            sql = """SELECT id, hash, salt 
                     FROM {}
                     WHERE username = ? """.format(self.USERS_TABLE_NAME)
            
            self.c.execute(sql, (username,))
            result = self.c.fetchone()
            # self.commit()
            
            return {'id': result[0], 'hash': result[1], 'salt': result[2]}

        except Exception as e:
            print(e)
            # self.rollback
            # return None



    def delete_account(self, account_id=None, owner_id=None):
        """ """
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


    def is_new_username(self, username):

        if not isinstance(username, str):
            raise TypeError('Username is not of type string.')

        self.begin_transaction()

        try:
            query = """SELECT COUNT(*) as COUNT FROM {} WHERE username = ?""".format(self.USERS_TABLE_NAME)

            self.c.execute(query, (username, ))
            result = self.c.fetchone()[0] # Gets the scalar count value.
            self.commit()
        except Exception as e:
            print(e)
            result = None
            self.rollback()

        if result != None:
            return result <= 0
        else:
            return False


if __name__ == "__main__":
    db = DatabaseHandler("vault")
    db.is_new_username('test')
