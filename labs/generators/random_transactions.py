import datetime
import json
import random
import uuid

from faker import Faker

fake = Faker()


def generate_transactions(num_transactions=25):  # Parameter for number of transactions

    transactions = []

    for _ in range(num_transactions):
        customer_id = random.randint(1, 1000)
        num_items = random.randint(1, 15)
        items = []
        total_amount = 0

        for _ in range(num_items):
            product_name = fake.color_name() + " " + fake.random_element(
                elements=('Shirt', 'Pants', 'Shoes', 'Hat', 'Socks'))  # Fix: Combine color and item

            quantity = random.randint(1, 5)
            price = round(random.uniform(5.0, 200.0), 2)
            item_total = quantity * price
            total_amount += item_total

            items.append({
                "product_name": product_name,
                "quantity": quantity,
                "price": price,
                "item_total": item_total
            })

        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "customer_id": customer_id,
            "transaction_date": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            "items": items,
            "total_amount": round(total_amount, 2),
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            "shipping_address": fake.address(),
            "ip_address": fake.ipv4(),
            "device": random.choice(['Mobile', 'Tablet', 'Desktop']),
            "browser": fake.user_agent(),
            "status": random.choice(["Completed", "Pending", "Cancelled", "Refunded"]),
            "promo_code": random.choices([fake.uuid4(), None], weights=[0.3, 0.7])[0],

        }
        transactions.append(transaction)

    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"../../data/transactions/transactions_{timestamp}.json"  # New line delimited JSON

    with open(filename, 'w') as jsonfile:
        for transaction in transactions:
            json.dump(transaction, jsonfile)  # Dump each transaction separately
            jsonfile.write('\n')  # Add newline delimiter

    print(f"New line delimited JSON file '{filename}' created successfully with {num_transactions} transactions.")


# Example usage to generate 50 transactions:
generate_transactions(random.randint(9, 99))
