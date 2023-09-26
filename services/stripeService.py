import stripe
import json
from settings.config import STRIPE_CONFIG
from services.dbservice import update_record_in_db
from model.models import Customer, CustomerDB

stripe.api_key = STRIPE_CONFIG['api_key']

def update_stripe_customer(customer_id, changes):
    try:
        stripe_customer = stripe.Customer.retrieve(customer_id)
        if changes is not None:
            for key, value in changes.items():
                stripe_customer[key] = value
        stripe_customer.save()
    except stripe.error.StripeError as e:
        return f"Stripe error updating customer {customer_id}: {e}"
    except Exception as e:
        return f"Error updating customer {customer_id}: {e}"

def create_stripe_customer(id, customer_data):
    try:
        stripe_customer = stripe.Customer.create( name=customer_data['name'], email=customer_data['email'])
        stripe_customer["stripe_id"] = stripe_customer['id']
        stripe_customer["id"] = id
        db_customer = update_record_in_db(CustomerDB, id, Customer, stripe_customer)
    except stripe.error.StripeError as e:
        return f"Stripe error creating customer: {e}"
    except Exception as e:
        return f"Error creating customer: {e}"

def delete_stripe_customer(customer_id):
    try:
        stripe.Customer.delete(customer_id)
        return f"Deleted Stripe customer {customer_id}"
    except stripe.error.StripeError as e:
        return f"Stripe error deleting customer {customer_id}: {e}"
    except Exception as e:
        return f"Error deleting customer {customer_id}: {e}"