# Python packages imports
import sqlite3
import re

# lib imports
from lib import Account, User

# Handler imports
from AuthenticationHandler import AuthenticationHandler
from DatabaseHandler import DatabaseHandler


class Model:

    def __init__(self, db_name='vault'):
        self.db_handler = DatabaseHandler(db_name)
        self.auth_handler = AuthenticationHandler()
        

    def add_new_account(self, account):

        if not isinstance(account, Account.Account):
            raise TypeError("account must be of type Account")

        self.db_handler.insert_new_account(account)


if __name__ == "__main__":
    db = Model("vault")
    acc =  Account.Account("type", "user", "pass", "salt", 1)
    db.add_new_account(acc)
