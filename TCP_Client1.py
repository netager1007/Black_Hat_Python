import socket
#target_host = "192.168.1.128"
target_host = "localhost"
target_port = 9999

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