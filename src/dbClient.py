#!/usr/bin/python
import paho.mqtt.client as mqtt

server_addr = "127.0.0.1"
topic = '$sensor/#'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #Insert data to MongoDB

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server_addr)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
