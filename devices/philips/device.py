
import json
import os
import random
import time

import paho.mqtt.client as mqtt


BROKER = os.getenv("BROKER", "mosquitto")
DEVICE_VERSION = os.getenv("DEVICE_VERSION", "v1")

client_id = f"philips_{BROKER}_{DEVICE_VERSION}"
client = mqtt.Client(client_id)
client.connect(BROKER, 1883, 60)



while True:
    payload = {
        "state": random.choice(["ON", "OFF"]),
        "brightness": random.randint(0, 100),
        "device_version": DEVICE_VERSION,
        "broker": BROKER,
    }
    
    topic = f"hue/{BROKER}/{DEVICE_VERSION}/light"
    client.publish(topic, json.dumps(payload), qos=0)
    print(f"Philips[{DEVICE_VERSION}] -> {BROKER}:", payload)
    time.sleep(3)