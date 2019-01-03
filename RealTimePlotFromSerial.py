
import threading
import time

def help_cmd_handle():
    print('help function')


cmd_dict = {'help': help_cmd_handle}


class CLIThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name

    def run(self):
        while 1:
            usr_input = input("> ")
            user_input_split = usr_input.lower().split(' ')  # make sure the command is in lowercase
            if user_input_split[0] == 'quit':
                break
            for cmd, function in cmd_dict.items():
                if user_input_split[0] == cmd:
                    function()
        print('quit main function')


class SerialThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name

    def run(self):
        while 1:
            print(self.thread_name)
            time.sleep(5)


def main():
    cli_thread = CLIThread(1, "CLI_Thread")
    serial_thread = SerialThread(2, "SerialThread")
    serial_thread.start()
    cli_thread.start()
    cli_thread.join()
    serial_thread.join()


main()
