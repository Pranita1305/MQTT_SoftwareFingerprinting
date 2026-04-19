import time, random
import paho.mqtt.client as mqtt

client = mqtt.Client("sonoff_switch")
client.connect("nanomq", 1883, 60)

while True:
    state = random.choice(["ON", "OFF"])
    client.publish("sonoff/power", state, qos=1)
    print("Sonoff:", state)
    time.sleep(2)