# app/data/db.py
import sqlite3
from pathlib import Path

# Folder that holds the database file and CSVs
DATA_DIR = Path("DATA")
DATA_DIR.mkdir(exist_ok=True)  # make sure folder exists

# Full path to database file
DB_PATH = DATA_DIR / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.

    Args:
        db_path: Path to the database file

    Returns:
        sqlite3.Connection: Database connection object
    """
    return sqlite3.connect(str(db_path))
