# Replacing Netcat
# ----------------
import sys
import socket
import getopt
import threading
import subprocess

# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("netcat Net Tool")
    print('')
    print("Usage: netcat.py -t target_host -p port")
    print("-l --listen - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]")
    print('')
    print('')
    print("Examples: ")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./netcat.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def document_it(func):
    def new_function(*args, **kwargs):
        print('Running function:', func.__name__)
        print('Positional arguments:', args)
        print('Keyword arguments:', kwargs)
        result = func(*args, **kwargs)
        print('Result:', result)
        return result
    return new_function

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to our target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer.encode())

        while True:
            # now wait for data back
            recv_len = 1
            response = b""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response.decode())

            # wait for more input
            buffer = input()
            buffer += "\n"

            # send it off
            client.send(buffer.encode())

    except Exception as e:
        print("[*] Exception! Exiting.", e)
        # tear down the connection
        client.close()


def run_command(command):
    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # send the output back to the client
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        # read in all of the bytes and write to our destination
        file_buffer = b""

        # keep reading data until none is available
        data = b''
        while b'\n' not in data:
            data += client_socket.recv(1024)
            print('[*] upload_destination data, type(data):', data, type(data))

        file_buffer = data
        print('[*] file_buffer:', file_buffer)

        # now we take these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
#            file_descriptor = open(upload_destination, "wt")

            file_descriptor.write(file_buffer)
            file_descriptor.close()

            print('[*] file_descriptor End ... write file_buffer:', file_buffer)

            # acknowledge that we wrote the file out
#            client_socket.send("Successfully saved file to %s\r\n" % upload_destination.encode())
            client_socket.send("Successfully saved file.".encode())
            print('[*] After client_socket.send OK!!!')

        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination.encode())

    # check for command execution
    if len(execute):
        # run the command
        output = run_command(execute)

        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            client_socket.send('<BHP:#> '.encode())

            # now we receive until we see a linefeed (enter key)
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            print('[*] client_handler command:', cmd_buffer)

            # send back the command output
            response = run_command(cmd_buffer.decode())

            # send back the response
            client_socket.send(response)


# @document_it
def server_loop():
    global target

    # if no target is defined, we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # spin off a thread to handle our new client

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))

        client_thread.start()


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", \
                                                ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
#        elif o in ("-c", "--commandshell"):
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
             port = int(a)
        else:
            assert False, "Unhandled Option"
    print('[*] listen:', listen, 'execute:', execute, 'command:', command, 'upload_dest:', upload_destination)

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input to stdin
        print('[*] sys.stdin.read() Start ... ')
        buffer = sys.stdin.read()
        print('[*] sys.stdin.read() buffer:', buffer)

        # send data off
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
        print('Function: Call Server_loop')
        server_loop()

main()


