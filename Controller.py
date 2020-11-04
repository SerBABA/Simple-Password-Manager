from Model import Model
from View  import View


class Controller():
    
    def __init__(self):

        self.model = Model()
        self.view = View()
        self.view.set_handler(self) 

        self.CMDS = {
            "sign_up": self.sign_up_handler
        }


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
            if self.model.sign_up_user(username, password):
                self.view.sign_up_form_success(response['msg'])
            else:
                self.view.sign_up_form_fail(response['msg'])
        else:
            self.view.sign_up_form_fail(response['msg'])


    def sign_in_handler(self):
        raise NotImplementedError()




if __name__ == "__main__":
    app = Controller()