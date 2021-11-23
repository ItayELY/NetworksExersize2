import socket
import sys

import watchdog
import string

serverIp = sys.argv[0]
serverPort = sys.argv[1]
folderPath = sys.argv[2]
timeToUpdate = sys.argv[3]
newFolder = True
if len(sys.argv) == 5:
    identifier = sys.argv[4]
    newFolder = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverIp, serverPort))

s.send(b'hello')
data = s.recv(100)
print("Server sent: ", data)

s.send(b'212356364')
data = s.recv(100)
print("Server sent: ", data)
s.close()