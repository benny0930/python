import socket

HOST = '192.168.56.56'
PORT = 1125

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world!')
    data = s.recv(1024)

print('Received:', data)