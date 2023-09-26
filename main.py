from fastapi import FastAPI, Request
from services.dbservice import create_record_in_db, update_record_in_db, delete_record_in_db
from model.models import Customer, CustomerDB
from Kafka.producer import publish_to_kafka
from settings.config import STRIPE_CONFIG
import stripe
import json

app = FastAPI()

@app.post("/webhook/stripe")
async def handle_stripe_webhook(request: Request):
    payload = await request.body()
    event = None
    payload_str = payload.decode('utf-8')
    payload_dict = json.loads(payload_str)

    try:
        event = stripe.Event.construct_from(
            payload_dict, STRIPE_CONFIG['api_key'], STRIPE_CONFIG['webhook_secret']
        )
    except ValueError as e:
        return {"error": str(e)}

    if event.type == 'customer.created':
        stripe_customer = event.data.object
        db_customer = create_record_in_db(CustomerDB, stripe_customer, Customer)
        return {"message": f"Customer created: {db_customer.id}"}
    elif event.type == 'customer.updated':
        stripe_customer = event.data.object
        db_customer = update_record_in_db(CustomerDB, stripe_customer['id'], Customer, stripe_customer)
        return {"message": f"Customer updated: {db_customer.id}"}
    elif event.type == 'customer.deleted':
        stripe_customer = event.data.object
        db_customer = delete_record_in_db(CustomerDB, stripe_customer['id'])
    return {"message": "Unhandled event type"}

@app.post("/customers")
async def create_customer(request: Request):
    payload = await request.body()
    payload_str = payload.decode('utf-8')
    stripe_customer = json.loads(payload_str)
    stripe_customer['stripe_id'] = "demo_id"
    create_record_in_db(CustomerDB, stripe_customer, Customer)
    message = publish_to_kafka(stripe_customer['id'], stripe_customer, 'stripe_customer', 'create')
    return {"message": message}


@app.patch("/customers/{customer_id}")
async def update_customer(customer_id: str, request: Request):
    payload = await request.body()
    payload_str = payload.decode('utf-8')
    stripe_customer = json.loads(payload_str)
    record = update_record_in_db(CustomerDB, customer_id, Customer, stripe_customer)
    message = publish_to_kafka(record.stripe_id, stripe_customer, 'stripe_customer', 'update')
    return {"message": message}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    record = delete_record_in_db(CustomerDB, customer_id)
    message = publish_to_kafka(record.stripe_id, None, 'stripe_customer', 'delete')
    return {"message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
