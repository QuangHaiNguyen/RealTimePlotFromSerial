print("hello world")


def help_cmd_handle():
    print('help function')


cmd_dict = {'help': help_cmd_handle}


def main():
    usr_input = ""
    while usr_input.lower() != 'quit':
        usr_input = input("> ")
        user_input_split = usr_input.lower().split(' ')  # make sure the command is in lowercase
        for cmd, function in cmd_dict.items():
            if user_input_split[0] == cmd:
                function()
    print('quit main function')


main()
