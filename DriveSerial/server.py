# -*- coding: utf-8 -*-
import socket
import os

if os.path.exists("D:\projects\tmp\python_unix_sockets_example"):
    os.remove("D:\projects\tmp\python_unix_sockets_example")

print("Opening socket...")
server = socket.socket(socket.AF_UNSPEC, socket.SOCK_DGRAM)
server.bind("D:\projects\tmp\python_unix_sockets_example")

print("Listening...")
while True:
    datagram = server.recv(1024)
    if not datagram:
        break
    else:
        print("-" * 20)
        print(datagram.decode('utf-8'))
        if "DONE" == datagram.decode('utf-8'):
            break
print("-" * 20)
print("Shutting down...")
server.close()
os.remove("D:\projects\tmp\python_unix_sockets_example")
print("Done")