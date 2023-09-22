## New Service Integration(example- Salesforce)
  I will explain by taking the example of Customer system integration of Salesforce. To implement real-time synchronization, I will make the following changes in my code:
  - In the services directory, I will add salesforce.py and define certain functions according to needs.
  - In main.py, define the new endpoint containing the salesforce webhook.
  - Write the salesforce configuration in config.py.
  - Include Kafka topic on salesforce_customer in consumer.py.
  - Now it can also work like stripe integration.
  I also was thinking about using abstraction but found the above method easier to implement.

## New System Integration(example- Integration of invoice in Stripe)
  - In models.py create a new model of the Invoice system.
  - Now create different APIs in the main.py about different events of invoice.
  - In consumer.py decode the Kafka topic name. (Kafka topic has to be produced in the form "service_system". eg: 'salesforce_invoice')
  - This implementation can be used similarly to that of Customer in stripe.
