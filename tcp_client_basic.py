import socket

#target_host = "www.google.com"
#target_port = 80
target_host = "192.168.1.128"
target_port = 21

# create a socket object
# socket.AF_INET : IPv4
# socket.SOCK_STREAM : TCP Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
# Binary Data Send
#client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode())

# receive Binary data
response = client.recv(4096)

print(response)
#print(response)