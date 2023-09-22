import stripe
from config import STRIPE_CONFIG
from dbservice import create_record_in_db, update_record_in_db, delete_record_in_db
from models import Customer, CustomerDB

stripe.api_key = STRIPE_CONFIG['api_key']

def update_stripe_customer(customer_id, changes):
    try:
        stripe_customer = stripe.Customer.retrieve(customer_id)
        if changes is not None:
            for key, value in changes.items():
                stripe_customer[key] = value
        stripe_customer.save()
        db_customer = update_record_in_db(CustomerDB, customer_id, Customer, stripe_customer)
        return f"Updated Stripe customer {db_customer.id}"
    except stripe.error.StripeError as e:
        return f"Stripe error updating customer {customer_id}: {e}"
    except Exception as e:
        return f"Error updating customer {customer_id}: {e}"

def create_stripe_customer(customer_data):
    try:
        stripe_customer = stripe.Customer.create( name=customer_data['name'], email=customer_data['email'])
        print(stripe_customer)
        db_customer = create_record_in_db(CustomerDB, stripe_customer, Customer)
        return f"Created Stripe customer {db_customer.id}"
    except stripe.error.StripeError as e:
        return f"Stripe error creating customer: {e}"
    except Exception as e:
        return f"Error creating customer: {e}"

def delete_stripe_customer(customer_id):
    try:
        db_customer = delete_record_in_db(CustomerDB, customer_id)
        stripe.Customer.delete(customer_id)
        return f"Deleted Stripe customer {customer_id}"
    except stripe.error.StripeError as e:
        return f"Stripe error deleting customer {customer_id}: {e}"
    except Exception as e:
        return f"Error deleting customer {customer_id}: {e}"