#!/usr/bin/python
'''
    Pull data from MQTT Server and store it in Mongo DB.
'''

import argparse
import datetime
import logging
import sys

import paho.mqtt.client as mqtt
from pymongo import MongoClient

VERSION = "0.1"

def db_client_handler(argv):
    '''
        Parses the command line args do the work.
    '''
    parser = argparse.ArgumentParser(description='''Pull data from MQTT server
                                                    and store it to the database''')
    parser.add_argument('--mqtt-host', default='localhost', help='''MQTT server address. Defaults
							            to "localhost"''')
    parser.add_argument('--mqtt-port', default='1883', type=int, help='''MQTT server port.
                  							 Defaults to 1883''')
    parser.add_argument('--mqtt-topic', default='sensor/', help='''Topic prefix to be used for
                                                 subscribing/publishing. Defaults to "sensor/"''')
    parser.add_argument('--log', help='''set log level to the specified value.
                                         Defaults to WARNING. Try DEBUG for maximum detail''')
    parser.add_argument('--syslog', action='store_true', help='enable logging to syslog')

    parser.add_argument('--db-type', default='mongo', help='''database server type. Defaults
							      to "mongo"''')
    parser.add_argument('--db-host', default='localhost', help='''database server address. Defaults
							          to "localhost"''')
    parser.add_argument('--db-port', default='27017', type=int, help='''database server port.
                  						       Defaults to 1883''')
    args = parser.parse_args(argv)


    if args.log:
        logging.getLogger().setLevel(args.log)
    if args.syslog:
        logging.getLogger().addHandler(logging.handlers.SysLogHandler())

    topic = args.mqtt_topic
    if not topic.endswith("/"):
        topic += "/"

    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    userdata = dict()
    userdata['topic'] = args.mqtt_topic
    userdata['dbType'] = args.db_type
    if userdata['dbType'] == 'mongo':
        userdata['dbClient'] = MongoClient(args.db_host, args.db_port)
        mqttc.on_message = on_message_db
    else:
        mqttc.on_message = on_message_print
    mqttc.user_data_set(userdata)
    mqttc.connect(args.mqtt_host)
    mqttc.loop_forever()

def on_connect(client, userdata, flags, return_code):
    '''
    The callback for when the client receives a CONNACK response from the server.
    '''
    print ('connected with result code ' + str(return_code) + ':' + str(flags) + ':' +
           str(userdata))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print 'subscribe to topic ' + userdata['topic']
    client.subscribe(userdata['topic'])

def on_message_print(client, userdata, msg):
    '''
    The callback for when a PUBLISH message is received from the server.
    '''
    print msg.topic  + str(msg.payload) + ':' + str(userdata) + ':' + str(client)


def on_message_db(client, userdata, msg):
    '''
    The callback for when a PUBLISH message is received from the server.
    '''
    print msg.topic  + str(msg.payload) + ':' + str(userdata) + ':' + str(client)
    dbClient = userdata['dbClient']
    db = dbClient['test-database']
    collection = db['sensor-data']
    document = { 'topic': msg.topic,
                 'data': msg.payload,
                 'time': datetime.datetime.now(),

    }
    post_id = collection.insert_one(document).inserted_id
    print post_id

if __name__ == "__main__":
    db_client_handler(sys.argv[1:])



