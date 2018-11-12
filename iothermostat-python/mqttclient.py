#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" mqttclient.py: Provides the MqttClient class, which interfaces with the Paho
    MQTT client for the IOThermostat package """

from time import sleep
import paho.mqtt.client as mqtt
import topics
import mqttconf

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class MqttClient:

    data_in = {} # topics as keys and messages as values
    client = None
    subscribelist = None
    
    def __init__(self,subscribelist=None):

        print("IOThermostat: Starting MQTT client..")

        self.subscribelist = subscribelist
        client_id = 'iothermostat-backend'
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.will_set(topics.IOTHERMSTATUS, 'Offline', qos=0, retain=True)

        self.client.username_pw_set(mqttconf.username, password=mqttconf.password)
        self.connect()

        print("IOThermostat: MQTT client active.")


    def connect(self):
        count = 1
        connectionOk = False

        while True:
            try:
                print("IOThermostat: MQTT client connecting..")
                self.client.connect(mqttconf.server, 
                                    mqttconf.port, 
                                    mqttconf.keepalive)
                self.client.loop_start()
                connectionOk = True
                break
            except ConnectionError:
                print('IOThermostat: MQTT client connection failed {} times, retrying in 5 seconds..'.format(count))
                count += 1
                sleep(5)
                
        if not connectionOk:
            raise ConnectionError(-1, 'Error: Can\'t connect to MQTT broker.')

    def on_disconnect(self,client, userdata,rc):

        rccodes = ['0: Connection successful',
                 '1: Connection refused - incorrect protocol version',
                 '2: Connection refused - invalid client identifier',
                 '3: Connection refused - server unavailable',
                 '4: Connection refused - bad username or password',
                 '5: Connection refused - not authorised'] 
        print( "IOThermostat: MQTT client disconnected (code {}).".format(rccodes[rc]) )

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):

        print("IOThermostat: MQTT client connected successfully.")
        self.publish({topics.IOTHERMSTATUS:'Active'})

        print("IOThermostat: MQTT client subscribing to: ")
        for topic in self.subscribelist:
            client.subscribe(topic)
            print('IOThermostat: {}'.format(topic))


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
    
        # paho mqtt gives 'bXXX' or bytes. convert this to UTF-8:
        msg.payload = msg.payload.decode("utf-8")
        #print( 'MQTT client received: {}: {}'.format(msg.topic,str(msg.payload)) )
        self.data_in[msg.topic] = str(msg.payload)

    def publish(self, data):
    
        # data is a dict with keys: topics and values: ['system/sensor': 'data']
        # usage: publish({'my/topic':'my message'})
        for topic in data.keys():
            self.client.publish(topic, data[topic], mqttconf.qos, mqttconf.retain)
            #print( 'MQTT: sent: {}: {}'.format(topic,data[topic]) )

    def getData(self):
    
        # clear data after read
        result = self.data_in
        self.data_in = {}
        # return dictionary with received topics and messages
        return result

    def close(self):
    
        # closes connection
        self.client.publish(topics.IOTHERMSTATUS, 'Offline', mqttconf.qos, mqttconf.retain)
        self.client.loop_stop()
        self.client.disconnect()
        print('IOThermostat: Stopped MQTT client.')
