from getpass import getpass

class View:

    def set_handler(self, controller):

        self.controller = controller


    def sign_up_form(self):
        """ """
        print('Please fill in the following details:')
        username = input('Choose username>>>')
        password = getpass('Choose password>>>')
        repeat_password = getpass('Repeat password>>')

        return username, password, repeat_password


    def sign_up_form_fail(self, message=''):

        if not isinstance(message, str):
            raise TypeError('Message provided is not of type string.')

        print('Sign up has failed!!!\n')
        print('Reason: {}'.format(message))


    def sign_up_form_success(self, message=''):

        if not isinstance(message, str):
            raise TypeError('Message provided is not of type string.')

        print('Sign up has succseeded\n')

        