class User:

    def __init__(self, username, password, user_id=None):
            self.id = user_id
            self.username=username
            self.password=password


    def __repr__(self):
        return "id: {}, username: {}, password: {}".format(self.id, 
        self.username, self.password)