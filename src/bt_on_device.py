#!/usr/bin/python
'''
This program is meant to be run on a BT enabled device, which is
already connected to the BT enabled hub. This simulates a sensor pushed
data to the BT enabled hub.
'''

import argparse
import datetime
import logging
import sys
import time

import bluetooth

def device_handler(argv):
    '''
        Parses the command line args and push the data to a BT Hub.
    '''
    parser = argparse.ArgumentParser(description='''
                                      Parses the command line args and push the data to a BT Hub.
                                    ''')
    parser.add_argument('--baddr', default=None, help='''BT Hub's MAC address.''')
    parser.add_argument('--bport', default=0x1001, type=int, help='''BT Hub's port.
                  							 Defaults to 1011''')
    parser.add_argument('--log', default='INFO', help='''set log level to the specified value.
                                         Defaults to WARNING. Try DEBUG for maximum detail''')
    parser.add_argument('--syslog', action='store_true', help='enable logging to syslog')
    args = parser.parse_args(argv)


    if args.log:
        logging.getLogger().setLevel(args.log)
    if args.syslog:
        logging.getLogger().addHandler(logging.handlers.SysLogHandler())


    if args.baddr is None:
        logging.error('BT addr not provided')
        sys.exit(2)

    bt_addr = args.baddr
    bt_port = args.bport

    bt_socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    logging.info('connected.  Adjusting link parameters.')

    logging.info('trying to connect to %s:%d', bt_addr, bt_port)
    bluetooth.set_l2cap_mtu(bt_socket, 65535)
    bt_socket.connect((bt_addr, bt_port))

    while True:
        data = datetime.datetime().now()
        sent = bt_socket.send(data)
        logging.info('sent packet of size %d (tried %d). Now sleeping for 5 seconds...',
                     sent, len(data))
        time.sleep(5)

    bt_socket.close()

if __name__ == "__main__":
    device_handler(sys.argv[1:])
