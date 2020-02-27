import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.147', 5560))

msg = s.recv(1024)
print(msg)
client_msg = "I am the CLIENT"

s.send(client_msg.encode())

s.close()