
import json
import os
import random
import time

import paho.mqtt.client as mqtt


BROKER = 'nanomq'

BROKER = os.getenv("BROKER", "mosquitto")
DEVICE_VERSION = os.getenv("DEVICE_VERSION", "v1")

client_id = f"sonoff_{BROKER}_{DEVICE_VERSION}"
client = mqtt.Client(client_id)
client.connect(BROKER, 1883, 60)


while True:
   
    payload = {
        "state": random.choice(["ON", "OFF"]),
        "device_version": DEVICE_VERSION,
        "broker": BROKER,
    }

    topic = f"sonoff/{BROKER}/{DEVICE_VERSION}/power"
    client.publish(topic, json.dumps(payload), qos=1)
    print(f"Sonoff[{DEVICE_VERSION}] -> {BROKER}:", payload)
    time.sleep(2)