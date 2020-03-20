# TCP Client
# ----------

import socket
target_host = "www.jbbank.co.kr"
target_port = 80

# create a socket object
# socket.AF_INET : IPv4
# socket.SOCK_STREAM : TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
# client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

msg = 'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'
client.send(msg.encode())    # Require Byte Str, so use msg.encode()
# receive some data
response = client.recv(4096)

print(response)
print(type(response))

# UDP Client
# ----------
import socket

target_host = "127.0.0.1"
target_port = 80

# create a socket object
# socket.AF_INT : IPv4
# socket.SOCK_DGRAM : UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto("AAABBBCCC".encode(), (target_host, target_port))

# receive some data
data, addr = client.recvfrom(4096)

print(data)

# TCP Server
# ----------
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip,bind_port))

# this is our client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)
    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send("ACK!")
    client_socket.close()

while True:
    client,addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()

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


