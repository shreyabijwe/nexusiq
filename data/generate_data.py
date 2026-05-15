import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="nexusiq",
    user="postgres",
    password="8090",
    port="5432"
)
cur = conn.cursor()

print("Connected to database...")

# Suppliers
print("Generating suppliers...")
for _ in range(50):
    cur.execute("""
        INSERT INTO suppliers (supplier_name, contact_email, phone, country, city)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        fake.company()[:100],
        fake.email()[:100],
        fake.phone_number()[:20],
        fake.country()[:50],
        fake.city()[:50]
    ))
conn.commit()
print("Suppliers done.")

# Products
print("Generating products...")
categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Sports', 'Toys', 'Beauty', 'Automotive']
for i in range(200):
    cur.execute("""
        INSERT INTO products (product_name, category, unit_price, supplier_id, sku)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        fake.catch_phrase()[:150],
        random.choice(categories),
        round(random.uniform(5.0, 999.99), 2),
        random.randint(1, 50),
        f"SKU-{i+1:05d}"
    ))
conn.commit()
print("Products done.")

# Customers
print("Generating customers...")
for _ in range(500):
    cur.execute("""
        INSERT INTO customers (full_name, email, phone, city, country)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        fake.name()[:100],
        fake.unique.email()[:100],
        fake.phone_number()[:20],
        fake.city()[:50],
        fake.country()[:50]
    ))
conn.commit()
print("Customers done.")

# Inventory
print("Generating inventory...")
for i in range(1, 201):
    cur.execute("""
        INSERT INTO inventory (product_id, quantity_in_stock, reorder_level, warehouse_location)
        VALUES (%s, %s, %s, %s)
    """, (
        i,
        random.randint(0, 1000),
        random.randint(5, 50),
        random.choice(['Warehouse A', 'Warehouse B', 'Warehouse C', 'Warehouse D'])
    ))
conn.commit()
print("Inventory done.")

# Orders + Order Items + Logistics
print("Generating orders...")
statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
carriers = ['FedEx', 'DHL', 'UPS', 'BlueDart', 'Aramex']

for i in range(10000):
    order_date = fake.date_time_between(start_date='-2y', end_date='now')
    delivery_date = order_date + timedelta(days=random.randint(2, 14))
    status = random.choice(statuses)
    customer_id = random.randint(1, 500)

    cur.execute("""
        INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_address, delivery_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING order_id
    """, (
        customer_id,
        order_date,
        status,
        round(random.uniform(10.0, 5000.0), 2),
        fake.address()[:200],
        delivery_date
    ))

    order_id = cur.fetchone()[0]

    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product_id = random.randint(1, 200)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(5.0, 999.99), 2)
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, product_id, quantity, unit_price, round(quantity * unit_price, 2)))

    cur.execute("""
        INSERT INTO logistics (order_id, carrier, tracking_number, dispatch_date, estimated_delivery, actual_delivery, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        order_id,
        random.choice(carriers),
        fake.uuid4()[:20],
        order_date + timedelta(days=1),
        delivery_date,
        delivery_date + timedelta(days=random.randint(-2, 3)) if status == 'delivered' else None,
        status
    ))

    if i % 1000 == 0:
        conn.commit()
        print(f"  {i}/10000 orders done...")

conn.commit()
print("All data generated successfully!")
print("Total orders: 10,000")

cur.close()
conn.close()