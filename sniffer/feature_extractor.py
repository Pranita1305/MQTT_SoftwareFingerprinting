import pyshark
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pcap_path = os.path.join(BASE_DIR, 'captures', 'mqtt_capture.pcap')

capture = pyshark.FileCapture(
    pcap_path,
    display_filter='mqtt'
)

dataset = []

def detect_device(topic, payload):
    if topic.startswith("hue/"):
        return "Philips"
    elif topic.startswith("miot/"):
        return "Xiaomi"
    elif topic.startswith("lg/"):
        return "LG"
    elif topic.startswith("sonoff/"):
        return "Sonoff"
    elif topic.startswith("sensor/"):
        return "RaspberryPi"
    return "Unknown"

def payload_type(payload):
    try:
        json.loads(payload)
        return "JSON"
    except:
        return "TEXT"

for packet in capture:
    try:
        mqtt = packet.mqtt

        topic = str(mqtt.topic)
        qos = int(mqtt.qos) if hasattr(mqtt, 'qos') else 0
        payload = str(mqtt.msg) if hasattr(mqtt, 'msg') else ""

        row = {
            "topic": topic,
            "qos": qos,
            "payload_type": payload_type(payload),
            "device": detect_device(topic, payload)
        }

        dataset.append(row)

    except Exception as e:
        continue

# Save CSV
csv_path = os.path.join(BASE_DIR, 'captures', 'dataset.csv')

with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["topic", "qos", "payload_type", "device"])
    writer.writeheader()
    writer.writerows(dataset)

print(f"Dataset created at {csv_path}")