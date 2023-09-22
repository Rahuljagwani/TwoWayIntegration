from confluent_kafka import Consumer, KafkaError
from config import CONSUMER_CONFIG
from TwoWayIntegration.services.stripeService import delete_stripe_customer, create_stripe_customer, update_stripe_customer
import json

consumer = Consumer(CONSUMER_CONFIG)
events = ['stripe_customer']
consumer.subscribe(events)
        
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print(f'Error: {msg.error().str()}')
    else:
        event_data = json.loads(msg.value())
        id = msg.key()
        id = id.decode('utf-8')
        if event_data is not None:
            topic = event_data['topic']
            event = event_data['event']
            del event_data['topic']
            del event_data['event']
        print(event_data)
        print(id)
        if event_data == None:
            delete_stripe_customer(id)
        elif event == 'update':
            update_stripe_customer(id, event_data)
        elif event == 'create':
            create_stripe_customer(event_data)
        
