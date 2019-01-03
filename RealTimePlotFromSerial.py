
import threading
import time
import queue
import serial


def help_cmd_handle():
    print('help function')


cmd_dict = {'help': help_cmd_handle}
msgQueue = queue.Queue(1)
msgQueue.put('stop')

comport = serial.Serial()
comport.baudrate = 115200
comport.port = 'COM9'


class CLIThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name

    def run(self):
        while 1:
            usr_input = input("")
            user_input_split = usr_input.lower().split(' ')  # make sure the command is in lowercase

            if user_input_split[0] == 'quit':
                msgQueue.put('quit')
                break
            elif user_input_split[0] in ('start', 'stop'):
                msgQueue.put(user_input_split[0])
            else:
                for cmd, function in cmd_dict.items():
                    if user_input_split[0] == cmd:
                        function()
                    else:
                        print('error')
        print('quit main function')


class SerialThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name

    def run(self):
        while 1:
            if not msgQueue.empty():
                msg = msgQueue.get()

            if msg == 'stop':
                comport.close()
                msg = 'idle'
            elif msg == 'start':
                if not comport.is_open:
                    comport.open()
                msg = 'read'
            elif msg == 'read':
                byte = comport.read()
                print(byte.decode())
            elif msg == 'quit':
                break;
            elif msg == 'idle':
                pass
            else:
                print('error')


cli_thread = CLIThread(1, "CLI_Thread")
serial_thread = SerialThread(2, "SerialThread")


def main():
    serial_thread.start()
    cli_thread.start()
    cli_thread.join()
    serial_thread.join()


main()
