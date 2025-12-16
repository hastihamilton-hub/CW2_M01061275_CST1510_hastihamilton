import pandas as pd
from pathlib import Path
from app.data.db import DATA_DIR


def load_csv_to_table(conn, csv_filename, table_name):
    """
    Load a CSV file into a database table using pandas.
    """
    # Build the full path to the CSV file inside the DATA directory
    csv_path = DATA_DIR / csv_filename

    # Check if the CSV file exists before attempting to load it
    if not csv_path.exists():
        print(f" CSV file not found: {csv_path}")
        return 0  # Return 0 rows loaded if file is missing

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Insert the DataFrame into the specified SQL table
    # - if_exists="append": adds data without deleting existing rows
    # - index=False: prevents pandas index from becoming a database column
    df.to_sql(
        name=table_name,
        con=conn,
        if_exists="append",
        index=False
    )

    # Count how many rows were loaded
    row_count = len(df)

    # Print a success message for logging/debugging purposes
    print(f" Loaded {row_count} rows from {csv_path.name} into '{table_name}' table.")

    # Return the number of rows inserted
    return row_count
