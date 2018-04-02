import bluetooth

bd_addr = "24:0A:64:1B:85:7D"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()

