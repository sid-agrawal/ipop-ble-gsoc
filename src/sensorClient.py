#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt


server_addr = "127.0.0.1"
sensor_set = 'sensor/heat'

mqttc = mqtt.Client()
mqttc.connect(server_addr)
temp = 1000
mqttc.publish(sensor_set, temp) 
mqttc.loop(2) #timeout = 2s
