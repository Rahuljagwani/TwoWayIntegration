from confluent_kafka import Producer, KafkaError
from config import PRODUCER_CONFIG
import json

producer = Producer(PRODUCER_CONFIG)
def publish_to_kafka(id, message, topic, event):
    try:
        if message is not None:
            message['topic'] = topic
            message['event'] = event
        message_value = json.dumps(message)
        producer.produce(topic, key=str(id), value=message_value)
        producer.flush()
        return {"Message added successfully,id":id}
    except KafkaError as e:
        print(f"Kafka error: {e}")
    except Exception as e:
        print(f"Error publishing to Kafka: {e}")

