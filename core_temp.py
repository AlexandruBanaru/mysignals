import json
import sys
import time
import logging

import paho.mqtt.publish as publish

MQTT_server = "mqtt.beia-telemetrie.ro"
MQTT_port = 1833
logger = logging.getLogger(__name__)

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp = ". ""))

def main():
    while True:

        temperature = measure_temp()
        topic = 'mysignals/raspberry/S1'

        data = {

        'Core temperature' : temperature

        }

        payload = json.dumps(data)
        publish.single(topic, qos = 1, hostname = MQTT_server, payload = payload)

        time.sleep(1)
if __name__ == '__main__':
    main()
