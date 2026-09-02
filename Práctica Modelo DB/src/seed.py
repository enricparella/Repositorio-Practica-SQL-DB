import argparse
import random
from datetime import timedelta

import pandas as pd
from faker import Faker
from google.cloud import bigquery

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

credentials_path = BASE_DIR / "credentials" / "service-account.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

fake = Faker("es_ES")

def parse_args():
    parser = argparse.ArgumentParser(description="Genera y carga datos sintéticos en BigQuery.")

    parser.add_argument("--project", required=True, help="ID del proyecto de Google Cloud.")
    parser.add_argument("--dataset", required=True, help="ID del dataset de BigQuery.")
    parser.add_argument("--customers", type=int, default=500, help="Número de clientes a generar.")
    parser.add_argument("--orders", type=int, default=2000, help="Número de pedidos a generar.")

    return parser.parse_args()

def setup_bigquery(project_id, dataset_id):
    client = bigquery.Client(project=project_id)

    dataset_ref = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset_ref.location = "EU"
    client.create_dataset(dataset_ref, exists_ok=True)

    print(f"Dataset preparado: {project_id}.{dataset_id}")

    return client

def create_table(client, project_id, dataset_id, table_name, schema):
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    table = bigquery.Table(table_id, schema=schema)
    client.create_table(table, exists_ok=True)

    print(f"Tabla preparada: {table_name}")

def create_tables(client, project_id, dataset_id):
    schema_customers = [
        bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("first_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("last_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("phone", "STRING"),
        bigquery.SchemaField("country", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("acquisition_channel", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("registration_date", "DATE", mode="REQUIRED"),
    ]

    schema_categories = [
        bigquery.SchemaField("category_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING"),
    ]

    schema_products = [
        bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("category_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING"),
        bigquery.SchemaField("sale_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("cost_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("stock", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("is_active", "BOOLEAN", mode="REQUIRED"),
    ]

    schema_orders = [
        bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("shipping_address", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("shipping_city", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("shipping_country", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("order_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("shipping_date", "DATE"),
        bigquery.SchemaField("delivery_date", "DATE"),
    ]

    schema_order_items = [
        bigquery.SchemaField("order_item_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("unit_price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("discount", "FLOAT"),
    ]

    schema_payments = [
        bigquery.SchemaField("payment_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("payment_method", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("payment_date", "DATE", mode="REQUIRED"),
    ]

    schema_reviews = [
        bigquery.SchemaField("review_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("order_item_id", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("rating", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("comment", "STRING"),
        bigquery.SchemaField("review_date", "DATE", mode="REQUIRED"),
    ]

    create_table(client, project_id, dataset_id, "customers", schema_customers)
    create_table(client, project_id, dataset_id, "categories", schema_categories)
    create_table(client, project_id, dataset_id, "products", schema_products)
    create_table(client, project_id, dataset_id, "orders", schema_orders)
    create_table(client, project_id, dataset_id, "order_items", schema_order_items)
    create_table(client, project_id, dataset_id, "payments", schema_payments)
    create_table(client, project_id, dataset_id, "reviews", schema_reviews)

def generate_customers(num_customers):
    customers = []

    acquisition_channels = ["organic", "social_media", "email", "referral", "paid_ads"]

    for customer_id in range(1, num_customers + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "country": fake.country(),
            "city": fake.city(),
            "acquisition_channel": random.choice(acquisition_channels),
            "registration_date": fake.date_between(start_date="-3y", end_date="today"),
        })

    return pd.DataFrame(customers)

def generate_categories():
    categories = [
        {"category_id": 1, "name": "Smartphones", "description": "Teléfonos móviles y smartphones."},
        {"category_id": 2, "name": "Laptops", "description": "Ordenadores portátiles."},
        {"category_id": 3, "name": "Audio", "description": "Auriculares, altavoces y dispositivos de audio."},
        {"category_id": 4, "name": "Tablets", "description": "Tablets y dispositivos similares."},
        {"category_id": 5, "name": "Accessories", "description": "Accesorios y complementos electrónicos."},
    ]

    return pd.DataFrame(categories)

def generate_products():
    products = []

    product_names = {
        1: ["Nova", "Vertex", "Pulse", "Nexus", "Orion"],
        2: ["VertexBook", "NovaBook", "CoreBook", "NexusBook", "OrbitBook"],
        3: ["SonicBeat", "WaveSound", "PulseAudio", "EchoSound", "NovaSound"],
        4: ["NovaTab", "VertexTab", "NexusTab", "OrbitTab", "PulseTab"],
        5: ["PowerLink", "ConnectPro", "NovaGear", "CoreLink", "NexusGear"],
    }

    for product_id in range(1, 101):
        category_id = random.randint(1, 5)
        sale_price = round(random.uniform(20, 1500), 2)
        cost_price = round(sale_price * random.uniform(0.4, 0.8), 2)

        products.append({
            "product_id": product_id,
            "category_id": category_id,
            "name": f"{random.choice(product_names[category_id])} {product_id}",
            "description": fake.sentence(),
            "sale_price": sale_price,
            "cost_price": cost_price,
            "stock": random.randint(0, 200),
            "is_active": random.choice([True, True, True, False]),
        })

    return pd.DataFrame(products)

def generate_orders(num_orders, customers_df):
    orders = []
    statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]

    for order_id in range(1, num_orders + 1):
        customer = customers_df.sample(1).iloc[0]
        status = random.choice(statuses)

        order_date = fake.date_between(start_date=customer["registration_date"], end_date="today")
        shipping_date = None
        delivery_date = None

        if status == "shipped":
            shipping_date = order_date + timedelta(days=random.randint(1, 3))

        elif status in ["delivered", "returned"]:
            shipping_date = order_date + timedelta(days=random.randint(1, 3))
            delivery_date = shipping_date + timedelta(days=random.randint(1, 7))

        orders.append({
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "status": status,
            "shipping_address": fake.street_address(),
            "shipping_city": fake.city(),
            "shipping_country": fake.country(),
            "order_date": order_date,
            "shipping_date": shipping_date,
            "delivery_date": delivery_date,
        })

    return pd.DataFrame(orders)

def generate_order_items(orders_df, products_df):
    order_items = []
    order_item_id = 1

    for _, order in orders_df.iterrows():
        num_items = random.choice([1, 2, 2, 2, 3, 3])
        selected_products = products_df.sample(num_items)

        for _, product in selected_products.iterrows():
            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": random.randint(1, 3),
                "unit_price": product["sale_price"],
                "discount": random.choice([None, None, None, 0.05, 0.10, 0.15]),
            })

            order_item_id += 1

    return pd.DataFrame(order_items)

def generate_payments(orders_df, order_items_df):
    payments = []
    payment_methods = ["card", "paypal", "bank_transfer"]

    for _, order in orders_df.iterrows():
        items = order_items_df[order_items_df["order_id"] == order["order_id"]]

        amount = 0

        for _, item in items.iterrows():
            discount = item["discount"] if pd.notna(item["discount"]) else 0
            amount += item["quantity"] * item["unit_price"] * (1 - discount)

        if order["status"] == "pending":
            payment_status = "pending"
        elif order["status"] == "cancelled":
            payment_status = "failed"
        elif order["status"] == "returned":
            payment_status = "refunded"
        else:
            payment_status = "completed"

        payments.append({
            "payment_id": order["order_id"],
            "order_id": order["order_id"],
            "payment_method": random.choice(payment_methods),
            "status": payment_status,
            "amount": round(amount, 2),
            "payment_date": order["order_date"],
        })

    return pd.DataFrame(payments)

def generate_reviews(orders_df, order_items_df):
    reviews = []
    review_id = 1

    eligible_orders = orders_df[orders_df["status"].isin(["delivered", "returned"])]

    for _, order in eligible_orders.iterrows():
        items = order_items_df[order_items_df["order_id"] == order["order_id"]]

        for _, item in items.iterrows():
            if random.random() < 0.35:
                reviews.append({
                    "review_id": review_id,
                    "order_item_id": item["order_item_id"],
                    "rating": random.randint(1, 5),
                    "comment": fake.sentence(),
                    "review_date": order["delivery_date"] + timedelta(days=random.randint(0, 30)),
                })

                review_id += 1

    return pd.DataFrame(reviews)

def load_dataframe(client, project_id, dataset_id, df, table_name):
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()

        table = client.get_table(table_id)
        print(f"Tabla {table_name} cargada correctamente: {table.num_rows} registros")

    except Exception as error:
        print(f"Error al cargar la tabla {table_name}: {error}")

def main():
    args = parse_args()

    client = setup_bigquery(args.project, args.dataset)
    create_tables(client, args.project, args.dataset)

    customers_df = generate_customers(args.customers)
    categories_df = generate_categories()
    products_df = generate_products()
    orders_df = generate_orders(args.orders, customers_df)
    order_items_df = generate_order_items(orders_df, products_df)
    payments_df = generate_payments(orders_df, order_items_df)
    reviews_df = generate_reviews(orders_df, order_items_df)

    load_dataframe(client, args.project, args.dataset, customers_df, "customers")
    load_dataframe(client, args.project, args.dataset, categories_df, "categories")
    load_dataframe(client, args.project, args.dataset, products_df, "products")
    load_dataframe(client, args.project, args.dataset, orders_df, "orders")
    load_dataframe(client, args.project, args.dataset, order_items_df, "order_items")
    load_dataframe(client, args.project, args.dataset, payments_df, "payments")
    load_dataframe(client, args.project, args.dataset, reviews_df, "reviews")

    print("Seed completado correctamente.")


if __name__ == "__main__":
    main()