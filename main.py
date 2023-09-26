from fastapi import FastAPI, Request, HTTPException
from services.dbservice import create_record_in_db, update_record_in_db, delete_record_in_db
from model.models import Customer, CustomerDB
from Kafka.producer import publish_to_kafka
from settings.config import STRIPE_CONFIG
from database.psql import SessionLocal
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
        stripe_customer['stripe_id'] = stripe_customer['id']
        stripe_customer['id'] = stripe_customer['id'].split("_")[1]
        create_record_in_db(CustomerDB, stripe_customer, Customer)
        print(f"{stripe_customer['name']} successfully created")
        
    elif event.type == 'customer.updated':
        stripe_customer = event.data.object
        db = SessionLocal()
        existing_record = db.query(CustomerDB).filter(CustomerDB.stripe_id == stripe_customer['id']).first()
        db.close()
        if existing_record:
            stripe_customer['stripe_id'] = stripe_customer['id']
            stripe_customer['id'] = existing_record.id
            update_record_in_db(CustomerDB, stripe_customer['id'], Customer, stripe_customer)
            print(f"{stripe_customer['name']} successfully updated")
        else:
            raise HTTPException(status_code=404, detail=f"{CustomerDB.__name__} not found")

    elif event.type == 'customer.deleted':
        stripe_customer = event.data.object
        db = SessionLocal()
        existing_record = db.query(CustomerDB).filter(CustomerDB.stripe_id == stripe_customer['id']).first()
        db.close()
        if existing_record:
            stripe_customer['stripe_id'] = stripe_customer['id']
            stripe_customer['id'] = existing_record.id
            delete_record_in_db(CustomerDB, stripe_customer['id'])
            print(f"{stripe_customer['name']} successfully deleted")
        else:
            raise HTTPException(status_code=404, detail=f"{CustomerDB.__name__} not found")

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
