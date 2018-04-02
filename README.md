# ipop-ble-gsoc
Holds code for GSoC 2018 code for IPOP

The functionality desired is achieved using different mqtt clients:

1. sensor_client.py: This reads data from the bluetooth sensor, and publisheses the data to mqtt 
                     under the topic specified by the command line arg. There is also a mock 
                     implentation of the sensor Client, where is data is generated locally instead 
                     of being read via BT.

        usage: sensor_client.py [-h] [--mqtt-host MQTT_HOST] [--mqtt-port MQTT_PORT]
                         [--mqtt-topic MQTT_TOPIC] [--log LOG] [--syslog]
                         [--sensor-type SENSOR_TYPE]

        Pull data from BLE sensor(or mock the data), and push it to MQTT server

        optional arguments:
          -h, --help            show this help message and exit
          --mqtt-host MQTT_HOST
                                MQTT server address. Defaults to "localhost"
          --mqtt-port MQTT_PORT
                                MQTT server port. Defaults to 1883
          --mqtt-topic MQTT_TOPIC
                          Topic prefix to be used for subscribing/publishing.
                          Defaults to "sensor/"
          --log LOG             set log level to the specified value. Defaults to
                          WARNING. Try DEBUG for maximum detail
          --syslog              enable logging to syslog
          --sensor-type SENSOR_TYPE
                          Mock or bluetooth
        
2. db_client.py: This client subscribes for topic as specified in the command line arg
                 and stores the received data in mongodb. Here is the format of the data 
                 stored in mongo db:

        database name: test-database
        collection name: sensor-data
        document format:
        {       
                'topic': topic,
                'data': dataFromSensor,
                'time': current time,
        }       

        usage: db_client.py [-h] [--mqtt-host MQTT_HOST] [--mqtt-port MQTT_PORT]
                            [--mqtt-topic MQTT_TOPIC] [--log LOG] [--syslog]
                            [--db-type DB_TYPE] [--db-host DB_HOST]
                            [--db-port DB_PORT]

        Pull data from MQTT server and store it to the database

        optional arguments:
          -h, --help            show this help message and exit
          --mqtt-host MQTT_HOST
                                MQTT server address. Defaults to "localhost"
          --mqtt-port MQTT_PORT
                                MQTT server port. Defaults to 1883
          --mqtt-topic MQTT_TOPIC
                                Topic prefix to be used for subscribing/publishing.
                                Defaults to "sensor/"
          --log LOG             set log level to the specified value. Defaults to
                                WARNING. Try DEBUG for maximum detail
          --syslog              enable logging to syslog
          --db-type DB_TYPE     database server type. Defaults to "mongo"
          --db-host DB_HOST     database server address. Defaults to "localhost"
          --db-port DB_PORT     database server port. Defaults to 1883

3. bt_bt_on_device.py: The file is meant to be run on the BT device which has is
                       supposed to a BT sensor. This will run in a loop and
                       send the current date every 5 seconds. The --baddr argument
                       is the BT MAC addr of the BT enabled hub.

        usage: bt_on_device.py [-h] [--baddr BADDR] [--bport BPORT] [--log LOG]
                               [--syslog]

        Parses the command line args and push the data to a BT Hub.

        optional arguments:
          -h, --help     show this help message and exit
          --baddr BADDR  BT Hub's MAC address.
          --bport BPORT  BT Hub's port. Defaults to 1011
          --log LOG      set log level to the specified value. Defaults to WARNING.
                         Try DEBUG for maximum detail
          --syslog       enable logging to syslog
