from Controller import Controller

app = Controller()
try:
    while(True):        
        try:
            user_input = input("vault> ")
            app.command_handler(user_input)
        except NotImplementedError as e:
            print(e)

except KeyboardInterrupt:
    print('disconnecting...')

