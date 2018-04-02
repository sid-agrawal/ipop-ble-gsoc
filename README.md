# ipop-ble-gsoc
Holds code for GSoC 2018 code for IPOP

The functionality desired is achieved using different mqtt clients:

1. sensor Client: This reads data from the bluetooth sensor, and published the data to mqtt 
                  under the topic 'sensor/<type>/<id>'. There is also a mock implentation of the
                  sensor Client, where is data is generated locally instead of being read via BT.

        ./sensorClient.py -type <IP | BT> -mq <mqtt server add> [ -baddr <bt sensor mac addr> ]
2. database Client: This client subscribes for topic under sensor/ and stored the received data 
                        in mongo db. Here is the format of the data stored in mongo db
                        {       
                                'topic': topic,
                                'data': dataFromSensor,
                        }       
        ./dbClient -mq <mqtt server addr> -topic <topic to subscribe to>
3. 
