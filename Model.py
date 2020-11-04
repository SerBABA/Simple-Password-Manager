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


    def authenticate_username(self, username):

        response = {'status': 200, 'msg': 'Username is valid!'}

        format_response = self.auth_handler.valid_username_format(username)

        if format_response['status'] != 200:
            return format_response

        is_new_username = self.db_handler.is_new_username(username)
        
        if not is_new_username:
            return {'status': 400, 'msg': 'Username already exists!'}

        return response


    def authenticate_password(self, password, repeat_password):

        response = {'status': 200, 'msg': 'Password is valid!'}

        format_response = self.auth_handler.valid_password_format(password)

        if format_response['status'] != 200:
            return format_response

        if password != repeat_password:
            return {'status': 400, 'msg': 'Passwords do not match!'}

        return response


    def authenticate_sign_up_values(self, username, password, repeat_password):
        """ """
        response = {'status': 200, 'msg': 'Account has successfully been validated.'}

        username_response = self.authenticate_username(username)

        if username_response['status'] != 200:
            return username_response


        password_response = self.authenticate_password(password, repeat_password)

        if password_response['status'] != 200:
            return password_response

        return response


    def sign_up_user(self, username, password):
        raise NotImplementedError('Sign up to database has not been implemented!')


if __name__ == "__main__":
    db = Model("vault")
    acc =  Account.Account("type", "user", "pass", "salt", 1)
    db.add_new_account(acc)
