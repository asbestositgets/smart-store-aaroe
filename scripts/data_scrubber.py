import pandas as pd

class DataScrubber:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the DataScrubber with a DataFrame.
        
        Parameters:
            df (pd.DataFrame): The DataFrame to be scrubbed.
        """
        self.df = df

    def check_data_consistency_before_cleaning(self) -> dict:
        """
        Check data consistency before cleaning by calculating counts of null and duplicate entries.
        
        Returns:
            dict: Dictionary with counts of null values and duplicate rows.
        """
        null_counts = self.df.isnull().sum()
        duplicate_count = self.df.duplicated().sum()
        return {'null_counts': null_counts, 'duplicate_count': duplicate_count}

    def check_data_consistency_after_cleaning(self) -> dict:
        """
        Check data consistency after cleaning to ensure there are no null or duplicate entries.
        
        Returns:
            dict: Dictionary with counts of null values and duplicate rows, expected to be zero for each.
        """
        null_counts = self.df.isnull().sum()
        duplicate_count = self.df.duplicated().sum()
        assert null_counts.sum() == 0, "Data still contains null values after cleaning."
        assert duplicate_count == 0, "Data still contains duplicate records after cleaning."
        return {'null_counts': null_counts, 'duplicate_count': duplicate_count}

    def filter_column_outliers(self) -> pd.DataFrame:
        """
        Filter outliers in numeric columns using the IQR method.
        
        Returns:
            pd.DataFrame: Updated DataFrame with outliers removed from numeric columns.
        """
        for column in self.df.select_dtypes(include=['float64', 'int64']).columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            self.df = self.df[(self.df[column] >= (Q1 - 1.5 * IQR)) & (self.df[column] <= (Q3 + 1.5 * IQR))]
        return self.df

    def save_cleaned_data(self, output_file: str):
        """
        Save the cleaned DataFrame to a new CSV file.
        
        Parameters:
            output_file (str): The path where the cleaned DataFrame should be saved.
        """
        self.df.to_csv(output_file, index=False)


def clean_data(input_file: str, output_file: str):
    """
    Function to read data from the input file, clean the data, and save the cleaned data to the output file.
    
    Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path where the cleaned data will be saved.
    """
    # Read the input file
    df = pd.read_csv(input_file)

    # Initialize the DataScrubber with the DataFrame
    scrubber = DataScrubber(df)

    # Check consistency before cleaning
    print(f"Data consistency before cleaning for {input_file}:")
    print(scrubber.check_data_consistency_before_cleaning())

    # Filter outliers
    cleaned_df = scrubber.filter_column_outliers()

    # Check consistency after cleaning
    print(f"Data consistency after cleaning for {input_file}:")
    print(scrubber.check_data_consistency_after_cleaning())

    # Save the cleaned data
    scrubber.save_cleaned_data(output_file)
    print(f"Cleaned data saved to {output_file}")


# Define the file paths for each data file
input_file_customers = "data/prepared/customers_data_prepared.csv"
output_file_customers = "data/prepared/customers_data_cleaned.csv"

input_file_products = "data/prepared/products_data_prepared.csv"
output_file_products = "data/prepared/products_data_cleaned.csv"

input_file_sales = "data/prepared/sales_data_prepared.csv"
output_file_sales = "data/prepared/sales_data_cleaned.csv"

# Clean the data for customers
clean_data(input_file_customers, output_file_customers)

# Clean the data for products
clean_data(input_file_products, output_file_products)

# Clean the data for sales
clean_data(input_file_sales, output_file_sales)
