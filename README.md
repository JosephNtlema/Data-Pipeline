# Data-Pipeline
ETL Pipeline for Ingestion

Here's a `README.md` documentation for the ETL pipeline code that explains what needs to be installed and how to run the code successfully:

---

# ETL Pipeline for Customer Transactions

This is an ETL (Extract, Transform, Load) pipeline that extracts customer transaction data from an API, transforms the data into a structured format, and loads it into a PostgreSQL database.

### **Prerequisites**

Before running the ETL pipeline, make sure to install the following dependencies:

1. **Python** (Version 3.6+)
2. **PostgreSQL** database (Ensure PostgreSQL is installed and running locally or on a server)
3. **Python Packages**:
    - `requests`: For making HTTP requests to the API.
    - `pandas`: For data manipulation and transformation.
    - `psycopg2`: For connecting to the PostgreSQL database.

### **Install Dependencies**

To install the required Python packages, run the following command in your terminal or command prompt:

```bash
pip install requests pandas psycopg2
```

### **Setup and Configuration**

1. **API Key**:
   - You will need an API key to access the API endpoint.
   - Contact the hiring manager, Adam, to receive your API key.

2. **Database Configuration**:
   - The pipeline loads the data into a PostgreSQL database.
   - Update the `db_url` variable in the script with the appropriate PostgreSQL connection string:
   
     ```python
     db_url = "postgresql://username:password@localhost/mydatabase"
     ```

     Replace `username`, `password`, `localhost`, and `mydatabase` with your actual PostgreSQL credentials and database information.

3. **API Endpoint**:
   - The pipeline fetches customer transaction data from a predefined API endpoint:
   
     ```
     https://8b1gektg00.execute-api.us-east-1.amazonaws.com/default/engineer-test
     ```

4. **Date Range**:
   - The pipeline is set to fetch transaction data for January 2023 (`start_date = "2023-01-01"`, `end_date = "2023-01-31"`).
   - You can modify these dates in the `start_date` and `end_date` variables to fetch data for different periods.

### **Running the Code**

To run the ETL pipeline, simply execute the script:

```bash
python etl_pipeline.py
```

This will:
1. **Extract** the transaction data from the API for the specified date range.
2. **Transform** the data by cleaning and converting it into a structured format.
3. **Load** the data into the PostgreSQL database.

### **Code Explanation**

1. **Extract Data**:
   - A `POST` request is sent to the API endpoint with the specified date range in the request body.
   - The response is expected to be a JSON object containing the transaction data.

2. **Transform Data**:
   - The data is converted into a `pandas` DataFrame.
   - The column names are cleaned (lowercased and spaces replaced with underscores).
   - The `transaction_date` column is converted to `datetime`.
   - Rows with missing critical fields (e.g., `customer_id`, `product_id`, `transaction_amount`) are dropped.

3. **Load Data**:
   - A connection to the PostgreSQL database is established using `psycopg2`.
   - The table is created if it doesn't exist, and the transformed data is inserted into the database.

### **Database Table Schema**

The pipeline assumes the following schema for the `customer_transactions` table:

```sql
CREATE TABLE IF NOT EXISTS customer_transactions (
    customer_id INT,
    product_id INT,
    transaction_date DATE,
    transaction_amount FLOAT,
    transaction_type VARCHAR(50),
    product_category VARCHAR(50)
);
```

### **Error Handling**

- If the API request fails, the pipeline raises an exception with the corresponding error message.
- Missing data in critical fields (`customer_id`, `product_id`, `transaction_amount`) will result in rows being dropped.

### **Troubleshooting**

1. **ModuleNotFoundError**: Ensure all required Python packages are installed. Use the command:
   ```bash
   pip install requests pandas psycopg2
   ```

2. **PostgreSQL Connection Error**: Verify that PostgreSQL is installed, running, and that the connection string (`db_url`) is correctly configured.

3. **Invalid API Key**: Ensure that the correct API key is passed in the request header.

### **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---
