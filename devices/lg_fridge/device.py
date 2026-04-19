import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client("lg_fridge")
client.connect("hivemq", 1883, 60)

while True:
    payload = {
        "temp": random.randint(2, 8),
        "door": random.choice(["open", "closed"]),
        "status": "running"
    }
    client.publish("lg/fridge/status", json.dumps(payload), qos=1)
    print("LG:", payload)
    time.sleep(6)