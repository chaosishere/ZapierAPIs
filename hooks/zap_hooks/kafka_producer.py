from confluent_kafka import Producer

def create_kafka_producer():
    config = {
        'bootstrap.servers': 'localhost:9092',  # Kafka server in Docker
        'client.id': 'django_kafka_producer'
    }
    return Producer(config)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

