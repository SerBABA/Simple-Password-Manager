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
        self.MAX_GUESS_ATTEMPTS = 3
        self.MINIMUM_PASSWORD_LENGTH = 4
        self.is_owner = False



if __name__ == "__main__":
    app = Controller(Model(), View())