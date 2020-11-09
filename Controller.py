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
        return self.view.disconnect()


    def command_handler(self, message, token=None):
        if not isinstance(message, str):
            return self.view.build_response(400, 'Message given to command_handler was not of type string.')
        try:
            return self.CMDS[message]()
        except KeyError:
            return self.view.build_response(400, 'Unkown command')


    def sign_up_handler(self):
        """ """
        username, password, repeat_password = self.view.sign_up_form()
        response = self.model.authenticate_sign_up_values(username, password, repeat_password)

        if response['status'] == 200:
            response = self.model.sign_up_user(username, password)
            if response['status'] == 200:
                return self.view.sign_up_form_success(response['status'], response['msg'])
            else:
                return self.view.sign_up_form_fail(response['status'], response['msg'])
        else:
            return self.view.sign_up_form_fail(response['status'], response['msg'])


    def sign_in_handler(self):
        # get user details.
        username, password = self.view.sign_in_form()

        # compare is correct account
        response = self.model.authenticate_user_credentials(username, password)

        # store user id (some kind of token later on) and send message.
        if response['status'] == 200:
            return self.view.sign_in_form_success(response['token'])

        # Otherwise fail and send message.
        else:
            return self.view.sign_in_form_fail(response['status'], response['msg'])




if __name__ == "__main__":
    app = Controller()