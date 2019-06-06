import time
import serial
import json
import sys
import logging
import os

import paho.mqtt.publish as publish

MQTT_server = "mqtt.beia-telemetrie.ro"
MQTT_port = 1883
logger = logging.getLogger(__name__)
          
      
ser = serial.Serial(
              
               port='/dev/ttyACM0',
               baudrate = 115200,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           )
counter=0
          
def main():
    while True:
        x = ser.readline()
        y = x.decode('utf-8')
        z = y.splitlines()
        #y = y.replace("\r\n","")
        for line in z:
            v1 = str(line[0]) + str(line[1]) + str(line[2]) + str(line[3])+str(line[4])
            temperature = float(v1)
            topic =  'training/raspberrypi/alexandrubanaru'

            data = {"Body temperature":temperature}
            payload = json.dumps(data)
            publish.single(topic, qos = 1, hostname = MQTT_server, payload = payload)

            time.sleep(5)
if __name__ == '__main__':
    main()      


    

