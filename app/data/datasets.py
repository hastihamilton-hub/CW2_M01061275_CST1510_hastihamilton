import pandas as pd
from pathlib import Path

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection object
        csv_path: Path to CSV file
        table_name: Name of target table

    Returns:
        int: Number of rows loaded
    """

    csv_path = Path(csv_path)

    # 1. Check if file exists
    if not csv_path.exists():
        print(f" CSV not found: {csv_path}")
        return 0

    # 2. Read CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f" Error reading CSV: {e}")
        return 0

    try:
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists="append",
            index=False
        )
    except Exception as e:
        print(f" Error inserting into table '{table_name}': {e}")
        return 0

    print(f" Loaded {len(df)} rows from {csv_path.name} into '{table_name}'")
    return len(df)
