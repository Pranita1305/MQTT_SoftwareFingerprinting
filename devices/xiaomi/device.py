import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client("xiaomi_miot")
client.connect("emqx", 1883, 60)

while True:
    payload = {
        "id": random.randint(1000, 9999),
        "method": "set_power",
        "params": [random.choice(["on", "off"])]
    }
    client.publish("miot/device/control", json.dumps(payload), qos=0)
    print("Xiaomi:", payload)
    time.sleep(4)