#!/usr/bin/python
'''
    Pull data from BLE sensor(or mock the data), and push it to MQTT server.
'''

import argparse
import logging
import sys
import time

import bluetooth
import paho.mqtt.client as mqtt

VERSION = "0.1"

def sensor_client_handler(argv):
    '''
        Parses the command line args and push the data to MQTT broker.
    '''
    parser = argparse.ArgumentParser(description='''Pull data from BLE sensor(or mock the data),
                                                    and push it to MQTT server''')
    parser.add_argument('--mqtt-host', default='localhost', help='''MQTT server address. Defaults
							            to "localhost"''')
    parser.add_argument('--mqtt-port', default='1883', type=int, help='''MQTT server port.
                  							 Defaults to 1883''')
    parser.add_argument('--mqtt-topic', default='sensor/', help='''Topic prefix to be used for
                                                 subscribing/publishing. Defaults to "sensor/"''')
    parser.add_argument('--log', default='INFO', help='''set log level to the specified value.
                                         Defaults to WARNING. Try DEBUG for maximum detail''')
    parser.add_argument('--syslog', action='store_true', help='enable logging to syslog')

    parser.add_argument('--sensor-type', default='mock', help='''Mock or bluetooth''')
    args = parser.parse_args(argv)


    if args.log:
        logging.getLogger().setLevel(args.log)
    if args.syslog:
        logging.getLogger().addHandler(logging.handlers.SysLogHandler())

    topic = args.mqtt_topic
    if not topic.endswith("/"):
        topic += "/"

    mqttc = mqtt.Client()
    mqttc.connect(args.mqtt_host)
    mqttc.loop_start()

    while True:
        sensor_data = get_data_from_bt_sensor()
        logging.info('publishing:%s:%s', topic, sensor_data)
        mqttc.publish(topic, sensor_data)

def get_data_from_sensor(sensor_type):
    '''
        Blocking call to get data from the sensor
    '''

    if sensor_type != 'bluetooth':
        time.sleep(5)
        return 1010
    return get_data_from_bt_sensor()

def get_data_from_bt_sensor():
    '''
        Blocking call to get data from the BT sensor
    '''
    server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    server_sock.bind(("", 0x1001))
    server_sock.listen(1)
    while True:
        logging.info('waiting for incoming connection')
        client_sock, address = server_sock.accept()
        logging.info('Accepted connection from %s', str(address))


        logging.info('waiting for data')
        while True:
            try:
                data = client_sock.recv(65535)
            except bluetooth.BluetoothError as exception:
                logging.warn(exception)
                break

            if len(data) == 0:
                break

            logging.info('received packet of size %d', len(data))
            return data

        client_sock.close()

        logging.info('connection closed')

    server_sock.close()

if __name__ == "__main__":
    sensor_client_handler(sys.argv[1:])
