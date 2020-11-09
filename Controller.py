from Model import Model
from View  import View


class Controller():
    
    def __init__(self):

        self.model = Model()
        self.view = View()
        self.view.set_handler(self) 

        self.CMDS = {
            "exit": self.disconnect,
            "sign_up": self.sign_up_handler,
            "sign_in": self.sign_in_handler
        }


    def disconnect(self):
        """ """
        self.model.disconnect()


    def command_handler(self, message):
        if not isinstance(message, str):
            raise TypeError('Message given to command_handler was not of type string.')

        try:
            self.CMDS[message]()
        except KeyError:
            print('Unkown command')


    def sign_up_handler(self):
        """ """
        username, password, repeat_password = self.view.sign_up_form()
        response = self.model.authenticate_sign_up_values(username, password, repeat_password)

        if response['status'] == 200:
            if self.model.sign_up_user(username, password)['status'] == 200:
                self.view.sign_up_form_success(response['msg'])
            else:
                self.view.sign_up_form_fail(response['msg'])
        else:
            self.view.sign_up_form_fail(response['msg'])


    def sign_in_handler(self):
        # get user details.
        username, password = self.view.sign_in_form()

        # compare is correct account
        response = self.model.authenticate_user_credentials(username, password)

        # store user id (some kind of token later on) and send message.
        if response['status'] == 200:
            token = response['token']
            self.view.sign_in_form_success()

            # Store TOKEN

        # Otherwise fail and send message.
        else:
            self.view.sign_in_form_fail()
            return None




if __name__ == "__main__":
    app = Controller()