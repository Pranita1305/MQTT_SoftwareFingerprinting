import csv
import json
import os
import subprocess
import pyshark

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pcap_path = os.path.join(BASE_DIR, "captures", "mqtt_capture.pcap")

capture = pyshark.FileCapture(pcap_path, display_filter="mqtt")
dataset = []


def detect_device(topic, payload):
    _ = payload
    topic = topic.lower()

    if "hue" in topic:
        return "Philips"
    if "lg" in topic:
        return "LG"
    if "miot" in topic:
        return "Xiaomi"
    if "sonoff" in topic:
        return "Sonoff"
    if "sensor" in topic:
        return "RaspberryPi"
    return "Unknown"

def extract_version(payload):
    try:
        data = json.loads(payload)
        return data.get("device_version", "unknown")
    except Exception:
        return "unknown"


def extract_broker(topic):
    parts = topic.split("/")
    if len(parts) > 1:
        return parts[1]
    return "unknown"


def payload_type(payload):
    try:
        json.loads(payload)
        return "JSON"
    except Exception:
        return "TEXT"
    
    
for packet in capture:
    try:
        mqtt = packet.mqtt
        topic = str(mqtt.topic) if hasattr(mqtt, "topic") else ""
        qos = int(mqtt.qos) if hasattr(mqtt, "qos") else 0
        payload = str(mqtt.msg) if hasattr(mqtt, "msg") else ""
        msg_type = int(mqtt.msgtype) if hasattr(mqtt, "msgtype") else -1

        row = {
            "topic": topic,
            "device": detect_device(topic, payload),
            "device_version": extract_version(payload),
            "broker": extract_broker(topic),
            "qos": qos,
            "payload_type": payload_type(payload),
            "payload_len": len(payload),
            "msg_type": msg_type,
        }

        dataset.append(row)
        
    except Exception:
        continue
    
    
csv_path = os.path.join(BASE_DIR, "captures", "dataset.csv")
fieldnames = [
    "topic",
    "device",
    "device_version",
    "broker",
    "qos",
    "payload_type",
    "payload_len",
    "msg_type",
]

with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset)

print(f"Dataset created at {csv_path} with {len(dataset)} rows")

