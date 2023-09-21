import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 80))
server.listen(5)

while True:
    connection, address = server.accept()
    data = connection.recv(512)
    print(data.decode("utf-8"))