import time, json, random
import paho.mqtt.client as mqtt

client = mqtt.Client("raspberry_sensor")
client.connect("mosquitto", 1883, 60)

while True:
    payload = {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2)
    }
    client.publish("sensor/pi", json.dumps(payload), qos=1)
    print("Pi:", payload)
    time.sleep(5)