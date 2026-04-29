import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# Kafka Consumer
consumer = KafkaConsumer(
    'user-interactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# MongoDB 
client = MongoClient("mongodb://localhost:27017/")
db = client["kafka_db"]
collection = db["aggregation"]

# In-memory storage
user_counts = {}
item_counts = {}
total_events = 0

for message in consumer:
    data = message.value

    user_id = data["user_id"]
    item_id = data["item_id"]

    user_counts[user_id] = user_counts.get(user_id, 0) + 1
    item_counts[item_id] = item_counts.get(item_id, 0) + 1
    total_events += 1

    avg_per_user = total_events / len(user_counts) if len(user_counts) > 0 else 0

    max_item = max(item_counts, key=item_counts.get) if item_counts else None
    min_item = min(item_counts, key=item_counts.get) if item_counts else None

    result = {
        "total_events": total_events,
        "average_interactions_per_user": round(avg_per_user, 2),
        "most_interacted_item": max_item,
        "least_interacted_item": min_item
    }

    # save to JSON
    with open("aggregations.json", "w") as f:
        json.dump(result, f, indent=4)

    print(result)