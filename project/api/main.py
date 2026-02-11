import os
import json
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI
from confluent_kafka import Producer
from models import UserRegistration


app = FastAPI()

kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_topic = os.getenv("KAFKA_TOPIC")

producer = Producer({
    'bootstrap.servers': kafka_bootstrap_servers
})


@app.post("/register")
def register_user(user: UserRegistration):
    user_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    
    user_data = {
        "user_id": user_id,
        "full_name": user.full_name,
        "email": user.email,
        "age": user.age,
        "phone": user.phone,
        "city": user.city,
        "created_at": created_at
    }
    
    message_json = json.dumps(user_data)
    
    producer.produce(
        topic=kafka_topic,
        value=message_json.encode('utf-8')
    )
    producer.flush()
    
    return {
        "status": "accepted",
        "message": "user published to kafka"
    }


@app.get("/health")
def health():
    return {"status": "ok"}