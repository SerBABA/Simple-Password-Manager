# Python packages imports
import sqlite3
import re

# lib imports
from lib import Account, User, EncryptionHandler

# Handler imports
from AuthenticationHandler import AuthenticationHandler
from DatabaseHandler import DatabaseHandler


class Model:

    def __init__(self, db_name='vault'):
        self.db_handler = DatabaseHandler(db_name)
        self.auth_handler = AuthenticationHandler()
        self.crypt = EncryptionHandler.EncryptionHandler()


    def disconnect(self):
        self.db_handler.disconnect()
        

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



    # need to sanatize against second order sql injection attacks...
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


    def authenticate_user_credentials(self, username, password):
        
        # get user credentials 
        user_creds = self.db_handler.get_user_creds(username)

        # otherwise fail
        if user_creds == None:
            return {'status': 403, 'msg': 'Username or password are invalid.'}
        else:
            
            # compare the candidate password to the hash. If successful return id as token.
            if self.crypt.compare_hash(password, user_creds['hash'], user_creds['salt']):

                # Generate and append the token.
                token = self.auth_handler.generate_token(user_creds['id'])

                if token == None:
                    return {'status': 500, 'msg': 'Something went wrong...'}
                else:
                    return {'status': 200, 'msg': 'User credentials are correct.', 'token': token}
            
            # Otherwise return nothing and clear the memory.
            else:
                user_creds = None
                return {'status': 403, 'msg': 'User credentials are invalid!'}


    def sign_up_user(self, username, password):

        # Hash the password using Bycrypt and get the os.random() salt.
        salt = self.crypt.generate_salt()
        password_hash = self.crypt.hash_password(password, salt)

        # Create User object...
        new_user = User.User(username, password_hash, salt)

        # Add the user to the database
        response = self.db_handler.insert_new_user(new_user)

        # on any errors return a fail response. Otherwise return a success response.
        if response['status'] != 200:
            return {'status': 500, 'msg': 'Something went wrong while adding the user.'}
        else:
            return response


        # raise NotImplementedError('Sign up to database has not been implemented!')


if __name__ == "__main__":
    db = Model("vault")
    acc =  Account.Account("type", "user", "pass", "salt", 1)
    db.add_new_account(acc)
