class AuthenticationHandler:

    def __init__(self):        
        
        self.GUESSES_REMAINING = 3
        self.MINIMUM_PASSWORD_LENGTH = 4
        self.is_owner = False