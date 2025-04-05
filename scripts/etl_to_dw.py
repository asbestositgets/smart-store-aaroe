import pandas as pd
import sqlite3

# Path to your cleaned CSV files
customers_file_path = '/Users/alijah/Projects/smart-store-aaroe/data/prepared/customers_data_cleaned.csv'
products_file_path = '/Users/alijah/Projects/smart-store-aaroe/data/prepared/products_data_cleaned.csv'
sales_file_path = '/Users/alijah/Projects/smart-store-aaroe/data/prepared/sales_data_cleaned.csv'

# Read the cleaned CSV files
print(f"Reading customers file: {customers_file_path}")
customers_df = pd.read_csv(customers_file_path)

print(f"Reading products file: {products_file_path}")
products_df = pd.read_csv(products_file_path)

print(f"Reading sales file: {sales_file_path}")
sales_df = pd.read_csv(sales_file_path)

print("CSV files loaded successfully.")

# Connecting to the database
db_path = '/Users/alijah/Projects/smart-store-aaroe/data/dw/smart_sales.db'
print("Connecting to database...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the schema for the database
print("Creating schema...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    unit_price REAL,
    stock_quantity INTEGER,
    subcategory TEXT
);
''')

# Check if 'storeid' column exists in the sale table, and add it if it doesn't
cursor.execute("PRAGMA table_info(sale);")
columns = [column[1] for column in cursor.fetchall()]

if 'storeid' not in columns:
    cursor.execute("ALTER TABLE sale ADD COLUMN storeid INTEGER;")
    print("Added column 'storeid' to the sale table.")
else:
    print("Column 'storeid' already exists in the sale table.")

# Check if 'campaignid' column exists in the sale table, and add it if it doesn't
if 'campaignid' not in columns:
    cursor.execute("ALTER TABLE sale ADD COLUMN campaignid INTEGER;")
    print("Added column 'campaignid' to the sale table.")
else:
    print("Column 'campaignid' already exists in the sale table.")

# Check if 'saleamount' column exists in the sale table, and add it if it doesn't
if 'saleamount' not in columns:
    cursor.execute("ALTER TABLE sale ADD COLUMN saleamount REAL;")
    print("Added column 'saleamount' to the sale table.")
else:
    print("Column 'saleamount' already exists in the sale table.")

# Check if 'discountpercent' column exists in the sale table, and add it if it doesn't
if 'discountpercent' not in columns:
    cursor.execute("ALTER TABLE sale ADD COLUMN discountpercent REAL;")
    print("Added column 'discountpercent' to the sale table.")
else:
    print("Column 'discountpercent' already exists in the sale table.")

# Check if 'paymenttype' column exists in the sale table, and add it if it doesn't
if 'paymenttype' not in columns:
    cursor.execute("ALTER TABLE sale ADD COLUMN paymenttype TEXT;")
    print("Added column 'paymenttype' to the sale table.")
else:
    print("Column 'paymenttype' already exists in the sale table.")

# Deleting existing records (optional based on requirement)
print("Deleting existing records...")
cursor.execute("DELETE FROM customer;")
cursor.execute("DELETE FROM product;")
cursor.execute("DELETE FROM sale;")
print("Existing records deleted.")

# Insert customer data
print("Inserting customer data...")
customers_df.columns = [col.lower() for col in customers_df.columns]  # Standardize column names
customers_df = customers_df[['name']]  # Selecting only the 'name' column from the customer data
customers_df.to_sql('customer', conn, if_exists='append', index=False)

print("Customer data inserted.")

# Insert product data
print("Inserting product data...")
products_df.columns = [col.lower() for col in products_df.columns]  # Standardize column names

# Check and rename columns if needed
required_columns = {
    'productid': 'product_id',
    'productname': 'product_name',
    'unitprice': 'unit_price',
    'stockquantity': 'stock_quantity'
}

for old_col, new_col in required_columns.items():
    if old_col in products_df.columns:
        products_df = products_df.rename(columns={old_col: new_col})

# Remove duplicates based on 'product_id' to avoid conflict
products_df = products_df.drop_duplicates(subset=['product_id'])

# Insert the product data
products_df.to_sql('product', conn, if_exists='append', index=False)
print("Product data inserted.")

# Insert sales data
print("Inserting sales data...")

# Standardize the column names for the sales table
sales_df.columns = [col.lower() for col in sales_df.columns]  # Standardize column names

# Check the column names after renaming
print("Sales DataFrame columns after renaming:")
print(sales_df.columns)

# Rename the columns to match the schema in the database
sales_columns_map = {
    'transactionid': 'transaction_id',
    'saledate': 'transaction_date',  # Rename 'saledate' to match the schema
    'productid': 'product_id',
    'customerid': 'customer_id',
    'quantitysold': 'quantity',
    'totalamount': 'total_amount'
}

for old_col, new_col in sales_columns_map.items():
    if old_col in sales_df.columns:
        sales_df = sales_df.rename(columns={old_col: new_col})

# Check the final column names after renaming
print("Sales DataFrame columns after renaming to match schema:")
print(sales_df.columns)

# Remove duplicates based on 'transaction_id' to avoid conflict
sales_df = sales_df.drop_duplicates(subset=['transaction_id'])

# Insert the sales data
try:
    sales_df.to_sql('sale', conn, if_exists='append', index=False)
    print("Sales data inserted.")
except sqlite3.IntegrityError as e:
    print(f"Error inserting sales data: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("ETL process completed successfully.")
