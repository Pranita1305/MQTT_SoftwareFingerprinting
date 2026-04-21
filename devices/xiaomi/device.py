
import json
import os
import random
import time

import paho.mqtt.client as mqtt


BROKER = os.getenv("BROKER", "emqx")
DEVICE_VERSION = os.getenv("DEVICE_VERSION", "v1")

client_id = f"xiaomi_{BROKER}_{DEVICE_VERSION}"
client = mqtt.Client(client_id)
client.connect(BROKER, 1883, 60)



while True:
    payload = {
        "state": "ON",
        "id": random.randint(1000, 9999),
        "method": "set_power",
        "params": [random.choice(["on", "off"])],
        "device_version": DEVICE_VERSION,
        "broker": BROKER,
    }
    
    topic = f"miot/{BROKER}/{DEVICE_VERSION}/device/control"
    client.publish(topic, json.dumps(payload), qos=0)
    print(f"Xiaomi[{DEVICE_VERSION}] -> {BROKER}:", payload)
    if DEVICE_VERSION == "v1":
        delay = 2
    elif DEVICE_VERSION == "v2":
        delay = 5
    else:
        delay = 3
    time.sleep(delay)