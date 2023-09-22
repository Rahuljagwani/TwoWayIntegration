from fastapi import FastAPI, HTTPException, Request
from dbservice import create_record_in_db, update_record_in_db, delete_record_in_db
from models import Customer, CustomerDB
from producer import publish_to_kafka
from config import STRIPE_CONFIG
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

@app.post("/stripe/customers")
async def create_customer(request: Request):
    payload = await request.body()
    payload_str = payload.decode('utf-8')
    stripe_customer = json.loads(payload_str)
    message = publish_to_kafka(stripe_customer['id'], stripe_customer, 'stripe_customer', 'create')
    return {"message": message}


@app.patch("/stripe/customers/{customer_id}")
async def update_customer(customer_id: str, request: Request):
    payload = await request.body()
    payload_str = payload.decode('utf-8')
    stripe_customer = json.loads(payload_str)
    message = publish_to_kafka(customer_id, stripe_customer, 'stripe_customer', 'update')
    return {"message": message}

@app.delete("/stripe/customers/{customer_id}")
def delete_customer(customer_id: str):
    publish_to_kafka(customer_id, None, 'stripe_customer', 'delete')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
