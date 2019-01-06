
import threading
import queue
import serial

msgQueue = queue.Queue(1)
msgQueue.put('stop')

comport = serial.Serial()
comport.baudrate = 115200
comport.port = 'COM9'


def help_cmd_handle():
    print('help function')


def comport_cmd_handle(com):
    print('comport: ' + com)


def baudrate_cmd_handle(baud):
    print('baudrate: ' + baud)


def databit_cmd_handle(num_of_bit):
    print('databit: ' + num_of_bit)


def stopbit_cmd_handle(num_of_bit):
    print('stopbit: ' + num_of_bit)


def parity_cmd_handle(parity_conf):
    print('parity: ' + parity_conf)


def serial_cmd_handle(cmd):
    msgQueue.put(cmd)


cmd_dict = {'help': help_cmd_handle,
            'comport': comport_cmd_handle,
            'baudrate': baudrate_cmd_handle,
            'databit': databit_cmd_handle,
            'stopbit': stopbit_cmd_handle,
            'parity': parity_cmd_handle,
            'serial': serial_cmd_handle}


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
            elif user_input_split[0] == 'help':
                cmd_dict[user_input_split[0]]()
            else:
                for cmd, function in cmd_dict.items():
                    if user_input_split[0] == cmd:
                        function(user_input_split[1])
        print('quit main function')


class SerialThread(threading.Thread):
    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name

    def run(self):
        while 1:
            if not msgQueue.empty():
                machine_state = msgQueue.get()

            if machine_state == 'stop':
                comport.close()
                machine_state = 'idle'
            elif machine_state == 'start':
                try:
                    if not comport.is_open:
                        comport.open()
                        machine_state = 'read'
                except:
                    print("error")
                    machine_state = 'idle'
            elif machine_state == 'read':
                byte = comport.read()
                print(byte.decode())
            elif machine_state == 'quit':
                break
            elif machine_state == 'idle':
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
