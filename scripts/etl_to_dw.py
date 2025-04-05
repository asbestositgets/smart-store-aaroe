import pandas as pd
import sqlite3
import pathlib
import sys
import os

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("/Users/alijah/Projects/smart-store-aaroe/data/dw")  # Updated to writable path
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("/Users/alijah/Projects/smart-store-aaroe/data/prepared")  # Updated CSV path

# Create directory for the data warehouse if it doesn't exist
os.makedirs(DW_DIR, exist_ok=True)

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    print("Dropping existing tables if they exist...")
    cursor.execute("DROP TABLE IF EXISTS customer")
    cursor.execute("DROP TABLE IF EXISTS product")
    cursor.execute("DROP TABLE IF EXISTS sale")
    print("Existing tables dropped.")
    
    print("Creating new tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            CustomerID INTEGER PRIMARY KEY,
            Name TEXT,
            Region TEXT,
            Join_date TEXT,
            LoyaltyPoints INTEGER,
            PreferredContactMethod TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            productid INTEGER PRIMARY KEY,
            productname TEXT,
            category TEXT,
            unitprice REAL,
            stockquantity INTEGER,
            subcategory TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            transactionid INTEGER PRIMARY KEY,
            saledate TEXT,
            customerid INTEGER,
            productid INTEGER,
            storeid INTEGER,
            campaignid INTEGER,
            saleamount REAL,
            discountpercent REAL,
            paymenttype TEXT,
            FOREIGN KEY (customerid) REFERENCES customer (CustomerID),
            FOREIGN KEY (productid) REFERENCES product (productid)
        )
    """)
    print("Tables created.")

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    print("Deleting existing records...")
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")  # Ensure products are deleted
    cursor.execute("DELETE FROM sale")
    print("Existing records deleted.")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df = customers_df.rename(columns={"JoinDate": "Join_date"})  # Ensure column names match schema
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)
    print(f"Inserted {len(customers_df)} customer records.")

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df = products_df.drop_duplicates(subset=['productid'])  # Remove duplicates based on productid
    products_df.to_sql("product", cursor.connection, if_exists="replace", index=False)  # Replace existing products
    print(f"Inserted {len(products_df)} product records.")

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)
    print(f"Inserted {len(sales_df)} sales records.")

def load_data_to_db() -> None:
    try:
        print(f"Connecting to database at {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_data_cleaned.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_data_cleaned.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_cleaned.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
        print("Data successfully committed to the database.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    load_data_to_db()
