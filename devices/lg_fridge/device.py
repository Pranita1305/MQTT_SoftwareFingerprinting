
import json
import os
import random
import time

import paho.mqtt.client as mqtt


BROKER = os.getenv("BROKER", "hivemq")
DEVICE_VERSION = os.getenv("DEVICE_VERSION", "v1")

client_id = f"lg_{BROKER}_{DEVICE_VERSION}"
client = mqtt.Client(client_id)
client.connect(BROKER, 1883, 60)

while True:
    payload = {
        "state": "ON",
        "temp": random.randint(2, 8),
        "door": random.choice(["open", "closed"]),
        "status": "running",
        "device_version": DEVICE_VERSION,
        "broker": BROKER,
    }
    
    topic = f"lg/{BROKER}/{DEVICE_VERSION}/fridge/status"
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"LG[{DEVICE_VERSION}] -> {BROKER}:", payload)
    if DEVICE_VERSION == "v1":
        delay = 2
    elif DEVICE_VERSION == "v2":
        delay = 5
    else:
        delay = 3
    time.sleep(delay)