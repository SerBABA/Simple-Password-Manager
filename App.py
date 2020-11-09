from Controller import Controller

if __name__ == "__main__":
    app = Controller()
    user_input = ""

    try:
        while(user_input != 'exit'):
            try:
                user_input = input('vault>> ')
                app.command_handler(user_input)
            except NotImplementedError:
                print('The feature you are currently trying to use is not implemented.')
                
        print('Disconnecting...')
    except KeyboardInterrupt:
        print('Disconnecting...')