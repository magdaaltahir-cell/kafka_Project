import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

types = ['click', 'view', 'purchase']

while True:
    data = {
        "user_id": random.randint(1,1000),
        "item_id": random.randint(1,500),
        "interaction_type": random.choice(types),
        "timestamp": datetime.now().isoformat()
    }

    producer.send("user-interactions", data)
    print(data)
    time.sleep(1)
