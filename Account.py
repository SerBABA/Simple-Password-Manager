class Account:

    def __init__(self, acc_type, username, password, salt, user_id=None, acc_id=None):
            self.id = acc_id
            self.user = user_id
            self.type = acc_type
            self.username = username
            self.password = password
            self.salt = salt

            self.repr_string = "id: {}, user: {}, type: {}, username: {}, password: {}, salt: {}"
            

    def __repr__(self):
        return self.repr_string.format(self.id, self.user, self.type,
        self.username, self.password, self.salt)