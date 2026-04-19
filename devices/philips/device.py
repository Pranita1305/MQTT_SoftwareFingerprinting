import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client("philips_hue")
client.connect("mosquitto", 1883, 60)

while True:
    payload = {
        "state": random.choice(["ON", "OFF"]),
        "brightness": random.randint(0, 100)
    }
    client.publish("hue/livingroom/light", json.dumps(payload), qos=0)
    print("Philips:", payload)
    time.sleep(3)