STRIPE_CONFIG = {
    "api_key": "sk_test_51NsWcnSETM5tPN1HpjVIsBMFGk9dSNmf9qtpBnP81OUxpzbHRK9RCe90X9DOmr8h4TZZDsQcZS9V3hxNKz8wkA6p00oHc8VfUI",
    "webhook_secret": "whsec_Zi7QLRkrbyu5QBw1K03bVHVHjDkk8b9v",
}

DB_CONNECTION_PARAMS = {
    "user": "rahul",
    "password": "mypass",
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