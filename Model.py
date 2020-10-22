import sqlite3
import Account
import User


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
 

    def close_conn(self):
        self.conn.close()


    def create_tables(self):
        # Creating encrypted accounts table for database
        try:
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

            # Creating users table
            self.c.execute("""CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            UNIQUE (username)
            );""".format(self.USERS_TABLE_NAME))

            self.c.execute("""CREATE TRIGGER IF NOT EXISTS ensureUserExists
            BEFORE INSERT ON {}
            FOR EACH ROW
            WHEN NOT EXISTS (SELECT * FROM {} WHERE id=new.user)
            BEGIN
                SELECT RAISE (ROLLBACK, 'Unknown user id.');
            END;
            """.format(self.STORED_ACCOUNTS_TABLE_NAME, self.USERS_TABLE_NAME))

            self.commit()
        except:
            self.rollback()


    def insert_new_account(self, new_account):
        """ """
        if not isinstance(new_account, Account.Account):
            raise TypeError("new_account must be of type Account")
        try:
            sql = """INSERT INTO {} (user, type, username, password, salt)
                VALUES (?, ?, ?, ?, ?)""".format(self.STORED_ACCOUNTS_TABLE_NAME)

            self.c.execute(sql, (new_account.user, new_account.type, new_account.username,
            new_account.password, new_account.salt))
        
            self.commit()
        except Exception as e:
            print(e)
            self.rollback()


        

if __name__ == "__main__":
    db = Model("vault.db")
    ac =  Account.Account("type", "user", "pass", "salt", 1)
    db.insert_new_account(ac)
        

