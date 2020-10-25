class Vault():

    def __init__(self):
        self.DATABASE_FILE_NAME = 'vault.db'
        self.MAX_GUESS_ATTEMPTS = 3
        self.MINIMUM_PASSWORD_LENGTH = 4

        self.db = None
        self.is_owner = False
        