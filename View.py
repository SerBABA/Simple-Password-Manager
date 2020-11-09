from getpass import getpass

class View:

    def set_handler(self, controller):
        self.controller = controller


    def disconnect(self):
        return self.build_response(200, "Disconnecting...")

    def sign_in_form(self):
        print('Please fill in the following details: ')
        username = input('Username>> ')
        password = getpass('Password>> ')
        return username, password

    def sign_in_form_fail(self, status_code, message):
        
        if not isinstance(message, str):
            raise TypeError('Message provided is not of type string.')

        msg = 'Sign in failed...\n' + 'Reason: {}'.format(message)
        return self.build_response(status_code, msg)
    

    def sign_in_form_success(self, token):
        return self.build_response(200, 'Successfully signed in!', token)


    def sign_up_form(self):
        """ """
        print('Please fill in the following details:')
        username = input('Choose username>> ')
        password = getpass('Choose password>> ')
        repeat_password = getpass('Repeat password>> ')

        return username, password, repeat_password


    def sign_up_form_fail(self, status_code, message):

        if not isinstance(message, str):
            raise TypeError('Message provided is not of type string.')
        if not isinstance(status_code, int):
            raise TypeError('status code provided is not of type integer.')

        msg = 'Sign up has failed!!!\n' + 'Reason: {}'.format(message)
        return self.build_response(status_code, msg)

    def sign_up_form_success(self, status_code, message):

        if not isinstance(message, str):
            raise TypeError('Message provided is not of type string.')
        if not isinstance(status_code, int):
            raise TypeError('status code provided is not of type integer.')

        return self.build_response(status_code, 'Sign up was successfull!')


    def build_response(self, status_code, msg, token=None):
        
        response = {'status': status_code, 'msg':msg}

        if token != None:
            response['token'] = token
            
        return response
