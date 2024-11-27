import requests
import pandas as pd
import psycopg2
from datetime import datetime

api_url = "https://8b1gektg00.execute-api.us-east-1.amazonaws.com/default/engineer-test"
api_key = "your_api_key_here"
start_date = "2023-01-01"
end_date = "2023-01-31"
db_url = "postgresql://username:password@localhost/mydatabase"
table_name = "customer_transactions"

def extract_data(api_url, api_key, start_date, end_date):
    headers = {"Authorization": f"Bearer {api_key}"}
    request_body = {"start_date": start_date, "end_date": end_date}
    response = requests.post(api_url, json=request_body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}, Message: {response.text}")

def transform_data(raw_data):
    df = pd.DataFrame(raw_data)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df = df.dropna(subset=['customer_id', 'product_id', 'transaction_amount'])
    return df

def load_data(df, db_url, table_name):
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    # Create table if not exists (simplified for this example)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        customer_id INT,
        product_id INT,
        transaction_date DATE,
        transaction_amount FLOAT,
        transaction_type VARCHAR(50),
        product_category VARCHAR(50)
    );
    """
    cur.execute(create_table_query)
    conn.commit()

    # Insert data into the table
    for _, row in df.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} (customer_id, product_id, transaction_date, transaction_amount, transaction_type, product_category)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

def run_etl_pipeline(api_url, api_key, start_date, end_date, db_url, table_name):
    raw_data = extract_data(api_url, api_key, start_date, end_date)
    df = transform_data(raw_data)
    load_data(df, db_url, table_name)
    print(f"ETL pipeline completed successfully and data loaded into {table_name}.")

run_etl_pipeline(api_url, api_key, start_date, end_date, db_url, table_name)
