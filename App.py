from Controller import Controller

if __name__ == "__main__":
    app = Controller()
    user_input = ""
    token = None

    try:
        while(user_input != 'exit'):
            try:
                user_input = input('vault>> ')
                
                if token == None:
                    response = app.command_handler(user_input)
                else:
                    response = app.command_handler(user_input, token)


                if response['status'] == 200: 
                    print(response['msg'])

                    token = response.get('token', None)
                else:
                    print(response['msg'])


            except NotImplementedError:
                print('The feature you are currently trying to use is not implemented.')
                
    except KeyboardInterrupt:
        response = app.disconnect()
        print(response['msg'])

    # exit(0)