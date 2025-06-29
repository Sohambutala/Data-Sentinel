import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='192.168.0.12:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "RTI"

def generate_dummy_json():
    return {
        "sensor_id": random.randint(1, 5),
        "timestamp": time.time(),
        "temperature": round(random.uniform(20.0, 40.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2)
    }

print(f"Producing test data to Kafka topic: {topic}...")
while True:
    data = generate_dummy_json()
    producer.send(topic, value=data)
    print("Sent:", data)
    time.sleep(0.25)
