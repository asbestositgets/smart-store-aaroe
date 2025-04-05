# smart-store-aaroe
BI project client 01
## Saving Changes to GitHub:

Here are the commands to save changes and push them to GitHub:

```bash
git add .
git commit -m "Update README with commands"
git push
## Loading the Project and Git

To get started with your project, follow these steps:

1. Navigate to your project directory:

```bash
cd /Users/alijah/Projects/smart-store-aaroe

### Explanation:
- **Loading the Project and Git**: This section walks the user through loading the project, initializing the git repository, adding files, committing, and pushing to GitHub.
- **Activating the Virtual Environment**: This section guides the user to navigate to the project directory and activate the virtual environment.
- Both sections have the necessary commands wrapped in **code blocks** to make them easy to follow.

### Result in `README.md`:

---

## Loading the Project and Git

To get started with your project, follow these steps:

1. Navigate to your project directory:

```bash
cd /Users/alijah/Projects/smart-store-aaroe

# Data Scrubber

This project includes a Python script for data scrubbing and testing.

## Running the Tests

To run the tests for data scrubbing, use the following command:

```bash
python3 tests/test_data_scrubber.py


ETL to Data Warehouse for Smart Store
This repository contains the ETL (Extract, Transform, Load) process for the Smart Store project, which loads cleaned customer, product, and sales data into an SQLite data warehouse for analysis.

Overview
The project consists of three major steps:

Extract - Read cleaned data from CSV files.

Transform - Perform any necessary transformations to ensure the data fits the database schema.

Load - Load the data into an SQLite database.

The final output is an SQLite database file (smart_sales.db) that contains the following tables:

customer

product

sale

Prerequisites
Python 3.x

pandas library (pip install pandas)

sqlite3 library (comes with Python by default)

SQLite database viewer (optional, for exploring the database)

File Structure
The following file structure is expected:

pgsql
Copy
/data
    /dw
        smart_sales.db  # SQLite database file
    /prepared
        customers_data_cleaned.csv
        products_data_cleaned.csv
        sales_data_cleaned.csv
/scripts
    etl_to_dw.py  # Python script to perform ETL operations
/README.md
Setup Instructions
Install the necessary libraries:

Ensure you have Python 3 and pandas installed.

bash
Copy
pip install pandas
Prepare your data:

The cleaned CSV files should be placed in the /data/prepared directory:

customers_data_cleaned.csv

products_data_cleaned.csv

sales_data_cleaned.csv

Ensure the SQLite database path is correct:

The script assumes the SQLite database (smart_sales.db) will be located in /data/dw/. If it doesn't exist, the script will create a new one.

Run the ETL script:

To run the ETL process, execute the following command:

bash
Copy
python3 scripts/etl_to_dw.py
The script will:

Drop and recreate the database tables (customer, product, sale).

Delete existing records in the tables.

Insert the cleaned data from the CSV files into the respective tables.

Check the SQLite Database:

After running the script, the smart_sales.db database will be populated with the cleaned data. You can open it using any SQLite viewer or query tool to confirm the data has been successfully loaded.

Example:

Open SQLite database file in VS Code or another SQLite viewer.

Check if the tables customer, product, and sale have been created and populated.

Key Steps in the ETL Process
Drop Existing Tables:

The script starts by dropping any existing tables in the database to ensure a fresh load each time.

python
Copy
cursor.execute("DROP TABLE IF EXISTS customer")
cursor.execute("DROP TABLE IF EXISTS product")
cursor.execute("DROP TABLE IF EXISTS sale")
Creating New Tables:

After dropping the old tables, the script creates new ones with the following schemas:

sql
Copy
CREATE TABLE IF NOT EXISTS customer (
    CustomerID INTEGER PRIMARY KEY,
    Name TEXT,
    Region TEXT,
    JoinDate TEXT,
    LoyaltyPoints INTEGER,
    PreferredContactMethod TEXT
)
Similarly, for product and sale tables, schemas are created to store the necessary information about products and sales transactions.

Inserting Data:

The cleaned data from the CSV files (customers_data_cleaned.csv, products_data_cleaned.csv, sales_data_cleaned.csv) is read into pandas DataFrames and then inserted into the corresponding database tables.

Customer data insertion:

python
Copy
customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)
Product data insertion:

python
Copy
products_df.to_sql("product", cursor.connection, if_exists="append", index=False)
Sales data insertion:

python
Copy
sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)
Error Handling:

The script includes error handling for cases like unique constraint violations (e.g., duplicate productid), and it ensures that any errors during the process are logged.

Example:

python
Copy
except sqlite3.IntegrityError as e:
    print(f"Error occurred: {e}")
Final Commit:

After all the data is successfully inserted, the changes are committed to the database:

python
Copy
conn.commit()
Troubleshooting
Database Path Errors:

If you receive an error about the database path not existing (OperationalError: unable to open database file), make sure the path to the database is correct.

The default database path is set to:

python
Copy
DB_PATH = pathlib.Path("/Users/alijah/Projects/smart-store-aaroe/data/dw/smart_sales.db")
Missing CSV Files:

Ensure the CSV files are located at /data/prepared/ and named correctly:

customers_data_cleaned.csv

products_data_cleaned.csv

sales_data_cleaned.csv

If any of the CSV files are missing or improperly named, the script will fail with a FileNotFoundError.

License
This project is licensed under the MIT License - see the LICENSE file for details.