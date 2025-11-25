import sqlite3
from pathlib import Path

# Folder where DATA files and CSVs exist
DATA_DIR = Path("DATA")

# Path to database file
DB_PATH = DATA_DIR / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the DATA folder and DB file if they don't exist.
    """

    # Make sure DATA directory exists
    DATA_DIR.mkdir(exist_ok=True)

    # Connect to database
    return sqlite3.connect(str(db_path))
