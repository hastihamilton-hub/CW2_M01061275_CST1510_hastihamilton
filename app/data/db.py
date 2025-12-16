import sqlite3
from pathlib import Path

# Directory that stores the database file and CSV data
DATA_DIR = Path("DATA")

# Ensure the DATA directory exists (creates it if missing)
DATA_DIR.mkdir(exist_ok=True)

# Full file path to the SQLite database
DB_PATH = DATA_DIR / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Create and return a connection to the SQLite database.

    If the database file does not exist, SQLite will
    automatically create it at the specified path.

    Args:
        db_path (Path): Path to the SQLite database file

    Returns:
        sqlite3.Connection: Active database connection
    """
    # Establish and return a connection to the database
    return sqlite3.connect(str(db_path))
