STRIPE_CONFIG = {
    "api_key": "YOUR_API_KEY",
    "webhook_secret": "YOUR_WEBHOOK_SECRET",
}

DB_CONNECTION_PARAMS = {
    "user": "rahul",
    "password": "YOUR_PASS",
    "host": "localhost",
    "port": "5432",
    "database": "customercatalog"
}

PRODUCER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'twowayintegration',
    'acks': 'all'
}

CONSUMER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'stripe_customer',
    'auto.offset.reset': 'earliest'
}