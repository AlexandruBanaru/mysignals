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
          
      
while True:
    x = ser.readline()
    
    y = x.decode('utf-8')
    z = y.splitlines()
    
    
    
    for line in z:
        v1 = str(line.split(' ')[0])+" "+str(line.split(' ')[1])+" "+str(line.split(' ')[2])+" "
        v2 = str(line.split(' ')[3]) + " " 
        v3 = str(line.split(' ')[4]) + " "
        v4 = str(line.split(' ')[5]) + " "
        temp = float(v2)
        ecg = float(v3)
        emg = float(v4)
        x_pos = float(line.split(' ')[0])
        y_pos = float(line.split(' ')[1])
        z_pos = float(line.split(' ')[2])
        topic='training/raspberrypi/alexandrubanaru'
        data = {"bodyTemperature":temp,
                "ECG":ecg,
                "EMG":emg}
        payload = json.dumps(data)
        publish.single(topic, payload=payload, hostname=MQTT_server, port=MQTT_port)
        f = open('position.txt', 'a') 
        f.write(v1)
        f.close()
        g = open('body_temp.txt', 'a')
        g.write(v2)
        g.close()
        h = open('ecg.txt', 'a')
        h.write(v3)
        h.close()
        k = open('emg.txt', 'a')
        k.write(v4)
        k.close()
        time.sleep(0.001)
#    first line ( values) the position x, y, z
#    second line is body temperature (in C degrees)
#    third line is ECG value 
#    fourth line is EMG value 
