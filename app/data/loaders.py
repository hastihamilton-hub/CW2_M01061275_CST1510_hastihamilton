import pandas as pd
from pathlib import Path
from app.data.db import DATA_DIR


def load_csv_to_table(conn, csv_filename, table_name):
    """
    Load a CSV file into a database table using pandas.
    """
    csv_path = DATA_DIR / csv_filename

    if not csv_path.exists():
        print(f" CSV file not found: {csv_path}")
        return 0

    # Read CSV
    df = pd.read_csv(csv_path)

    # Insert into SQL table
    df.to_sql(
        name=table_name,
        con=conn,
        if_exists="append",
        index=False
    )

    row_count = len(df)
    print(f" Loaded {row_count} rows from {csv_path.name} into '{table_name}' table.")
    return row_count
