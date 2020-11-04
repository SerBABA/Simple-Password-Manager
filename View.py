class View:

    def set_handler(self, controller):

        self.controller = controller

        self.CMDS = {
            "sign_up": self.controller.sign_up
        }

    def invoke_action(self, action):        
        try:
            self.CMDS[action]()
        except Exception as e:
            print('Unable to get action {}'.format(action))
            print()

    def serve(self):
        print("Welcome to the vault!!!")
        action = input("Action? ")
        self.invoke_action(action)
