import pandas as pd
from pathlib import Path


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Active database connection
        csv_path: Path to the CSV file
        table_name: Target database table name

    Returns:
        int: Number of rows successfully inserted
    """

    # Convert csv_path to a Path object (safe for file operations)
    csv_path = Path(csv_path)

    # -------------------------------------------------
    # Step 1: Check that the CSV file exists
    # -------------------------------------------------
    if not csv_path.exists():
        print(f" CSV not found: {csv_path}")
        return 0

    # -------------------------------------------------
    # Step 2: Read the CSV file into a pandas DataFrame
    # -------------------------------------------------
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        # Handle errors such as malformed CSV files
        print(f" Error reading CSV: {e}")
        return 0

    # -------------------------------------------------
    # Step 3: Insert DataFrame rows into the SQL table
    # -------------------------------------------------
    try:
        df.to_sql(
            name=table_name,   # target table name
            con=conn,          # active DB connection
            if_exists="append",# append data, do not overwrite
            index=False        # do not include DataFrame index
        )
    except Exception as e:
        # Handle SQL insertion errors
        print(f" Error inserting into table '{table_name}': {e}")
        return 0

    # -------------------------------------------------
    # Step 4: Confirm successful load
    # -------------------------------------------------
    print(f" Loaded {len(df)} rows from {csv_path.name} into '{table_name}'")

    # Return number of rows inserted
    return len(df)
