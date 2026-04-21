
import json
import os
import random
import time

import paho.mqtt.client as mqtt


BROKER = os.getenv("BROKER", "mosquitto")
DEVICE_VERSION = os.getenv("DEVICE_VERSION", "v1")

client_id = f"raspberry_{BROKER}_{DEVICE_VERSION}"
client = mqtt.Client(client_id)
client.connect(BROKER, 1883, 60)


while True:
    payload = {
        "state": "ON",
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "device_version": DEVICE_VERSION,
        "broker": BROKER,
    }
    
    topic = f"sensor/{BROKER}/{DEVICE_VERSION}/pi"
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"RaspberryPi[{DEVICE_VERSION}] -> {BROKER}:", payload)
    if DEVICE_VERSION == "v1":
        delay = 2
    elif DEVICE_VERSION == "v2":
        delay = 5
    else:
        delay = 3
    time.sleep(delay)