from Model import Model
from View  import View


class Controller():
    
    def __init__(self, model, view):

        if not isinstance(model, Model):
            raise TypeError('Model given to controller is not of class Model.')
        if not isinstance(view, View):
            raise TypeError('View given to controller is not of class View.')

        self.model = model
        self.view = view

        self.view.set_handler(self) 
        self.view.serve()


    def sign_up_event_handler(self):
        """
        docstring
        """
        print('Sign up')
        pass


if __name__ == "__main__":
    app = Controller(Model(), View())