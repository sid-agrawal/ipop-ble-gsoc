#!/usr/bin/python
import sys
import struct
import bluetooth

def usage():
    print("usage: l2-mtu client [options]")
    print("")
    print("l2-mtu client <addr>     to start in client mode and connect to addr")
    sys.exit(2)

if len(sys.argv) < 2: usage()

mode = sys.argv[1]
if mode not in [ "client", "server" ]: usage()

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
print("connected.  Adjusting link parameters.")
bluetooth.set_l2cap_mtu( sock, 65535 )

bt_addr = sys.argv[2]
print("trying to connect to %s:1001" % bt_addr)
port = 0x1001
sock.connect((bt_addr, port))


totalsent = 0 
for i in range(1, 65535, 100):
    pkt = "0" * i
    sent = sock.send(pkt)
    print("sent packet of size %d (tried %d)" % (sent, len(pkt)))

sock.close()
