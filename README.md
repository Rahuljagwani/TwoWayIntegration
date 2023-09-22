# TwoWayIntegration

**NOTE:** For Now, this will work only in Linux Systems. I have used UBUNTU 22.04. Make sure you have python3 installed in your system along with pip3. Also Docker must be installed in order to run Kafka locally.
It is necessary that you install Kafka from my docker-compose file otherwise error will come as local partitions will be set to 3 as mentioned in 4th step.
## Steps to deploy
- ### Install Postgresql
	- Follow the instructions given here: https://ubuntu.com/server/docs/databases-postgresql
	- Configure it according to your needs.
		
- ### Create a Free Test account on Stripe
	- Visit the Stripe website by going to the following URL: [https://stripe.com/](https://stripe.com/)
	- Sign Up for a Free Test Account
	- Verify Your Email Address
	- After completing the initial setup, you'll be directed to your Stripe Dashboard. This is where you'll manage your test account and access your API credentials.
	- In your Stripe Dashboard, navigate to the "Developers" section. This is where you can access your API credentials.
	- In the "API keys" section, you will find your test API Key and Secret Key. These keys will allow you to interact with Stripe's API in a sandbox/test environment.
   
		-   **Publishable Key**: This is used on the client side (e.g., in web forms) to interact with Stripe from your website or application.
		-   **Secret Key**: This is used on the server side to make secure API requests to Stripe.

 - ### Setup Webhook
	 - Install ngrok by executing two commands given below
    ```
    sudo snap install ngrok
    ngrok  http 8000
    ```
    
	- Ngrok will provide a public URL (e.g., `https://your-subdomain.ngrok.io`) that has to be used in the next step.
	- Navigate to the "Developers" section.
    
	- Under "Webhooks," click on "Add endpoint."
    
	- Enter the public Ngrok URL or the URL provided by Localtunnel in the "Endpoint URL" field. (Eg: if you got https://your-subdomain.ngrok.io then write https://your-subdomain.ngrok.io/webhook/stripe in the URL field)
	- Select the following events (customer.created, customer.updated, customer.deleted).
    
	- Save the webhook endpoint.

- ### Install Kafka and clone repository
	- Make sure you have docker installed on your system.
	- Clone the repository and set it up locally.
	- Now go in the directory where all files of the repository are there (where docker-compose.yml is present)
	- Run the command to start Kafka
		> docker-compose up -d
	- Logs can be seen by executing below command
		> docker-compose logs -f kafka

- ### Setup Config File
	- Edit config.py
   ```
	  STRIPE_CONFIG  = {
			"api_key": "Enter your Secret Key from stripe",
			"webhook_secret": "Enter webhook secret by clicking reveal in webhook tab of developers section"
		}
  
		DB_CONNECTION_PARAMS  = {
			"user": "username of postgresql",
			"password": "password",
			"host": "localhost",
			"port": "5432",
			"database": "database name"
		}
  
		PRODUCER_CONFIG  = {
			'bootstrap.servers': 'localhost:9092',
			'client.id': 'twowayintegration',
			'acks': 'all'
		}
  
	  CONSUMER_CONFIG  = {
			'bootstrap.servers': 'localhost:9092',
			'group.id': 'stripe_customer',
			'auto.offset.reset': 'earliest'
		}
   ```

- ### Run the script
	- In the main directory run following commands one by one
   ```
   pip3 install -r requirements
   python3 main.py
   ```
    - Open new terminal and execute in main directory
	```
	python3 customer.py
	```
- ### Inward Synchronization demo
	- Visit the Customers tab in your Stripe Dashboard
	- Perform creation, deletion and updation there, same changes will be reflected into your local psql database.
	- You can check your database by executing following commands in your terminal.
   ```
   psql -U your_username -d database_name
   database_name>> Select * from customers;
   ```
- ### Outward Synchronization demo
	- Open postman app
	- Create, Update or Delete in local database using below APIs
	    - Endpoint for creating: "/stripe/customers", Body: {"id":"", "name":"name", "email":"email"}, METHOD: POST
	    -  Endpoint for updating: "/stripe/customers/{customer_id}", Body: {anything you want to update in JSON form}, METHOD: PUT
	    - Endpoint for deleting: "/stripe/customers/{customer_id}", METHOD: DELETE
	 - You will see that along with local database, customers in your stripe account will update.
