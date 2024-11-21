import csv
import random
import uuid

from faker import Faker

fake = Faker()  # Initialize Faker

num_customers = 1000
num_columns = 20

customers = []

for i in range(num_customers):
    customer = {
        "customer_id": i + 1,
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "registration_date": fake.date_between(start_date='-5y', end_date='today'),
        "status": random.choice(["active", "inactive", "pending"]),  # Still using random choices for status
        "product": fake.word(),  # More diverse product names
        "quantity": random.randint(1, 10),
        "price": round(random.uniform(10.0, 100.0), 2),
        "order_date": fake.date_between(start_date='-3y', end_date='today'),
        "shipping_date": fake.future_date(end_date='+30d'),  # Simulate future shipping dates
        "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
        "order_status": random.choice(["Shipped", "Processing", "Delivered", "Cancelled"]),
        "last_login": fake.date_time_between(start_date='-1y', end_date='now'),
        "latitude": fake.latitude(),
        "longitude": fake.longitude(),
        "transaction_id": str(uuid.uuid4()),
        "ip_address": fake.ipv4(),
        "user_agent": fake.user_agent(),
    }
    customers.append(customer)

fieldnames = customers[0].keys()

with open('../../data/customers.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(customers)

print("CSV file 'customers.csv' created successfully.")
