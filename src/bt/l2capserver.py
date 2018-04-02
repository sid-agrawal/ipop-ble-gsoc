# file: l2capclient.py
# desc: Demo L2CAP server for pybluez.
# $Id: l2capserver.py 524 2007-08-15 04:04:52Z albert $

import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )

port = 0x1001

server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

data = client_sock.recv(1024)
print("Data received: ", str(data))

while data:
    client_sock.send('Echo => ' + str(data))
    data = client_sock.recv(1024)
    print("Data received:", str(data))

client_sock.close()
server_sock.close()
