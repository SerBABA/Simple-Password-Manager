from lib import EncryptionHandler

class AuthenticationHandler:

    def __init__(self):        
        
        self.MINIMUM_USERNAME_LENGTH = 4
        self.MINIMUM_PASSWORD_LENGTH = 4
        self.crypt = EncryptionHandler.EncryptionHandler()

        self.MAXIMUM_USERNAME_LENGTH = 20
        self.MAXIMUM_PASSWORD_LENGTH = 20        

        self.known_tokens = {}

    def valid_username_format(self, username):

        if not isinstance(username, str):
            raise TypeError('Username is not of type string.')

        response = {'status': 200, 'msg': 'Username is of valid format.'}

        if len(username) < self.MINIMUM_USERNAME_LENGTH:
            response = {'status': 400, 'msg': 'Username is shorter then min of {} characters.'.format(self.MINIMUM_USERNAME_LENGTH)}
            return response

        if len(username) > self.MAXIMUM_USERNAME_LENGTH:
            response = {'status': 400, 'msg': 'Username is longer then max of {} characters.'.format(self.MAXIMUM_USERNAME_LENGTH)}
            return response

        return response

    def generate_token(self, user_id):
        number_tries = 10
        token = self.crypt.generate_token()
        
        try:
            while number_tries > 0:
                self.known_tokens[token]
                token = self.crypt.generate_token()
                number_tries -= 1

            return None
            
        except KeyError:
            #token = 'tok ' + token
            self.known_tokens[token] = user_id
            return token

    def valid_password_format(self, password):
    
        if not isinstance(password, str):
            raise TypeError('Password is not of type string.')

        response = {'status': 200, 'msg': 'Password is of valid format.'}

        if len(password) < self.MINIMUM_PASSWORD_LENGTH:
            response = {'status': 400, 'msg': 'Password is shorter then min of {} characters.'.format(self.MINIMUM_PASSWORD_LENGTH)}
            return response

        if len(password) > self.MAXIMUM_PASSWORD_LENGTH:
            response = {'status': 400, 'msg': 'Password is longer then max of {} characters.'.format(self.MAXIMUM_PASSWORD_LENGTH)}
            return response

        return response