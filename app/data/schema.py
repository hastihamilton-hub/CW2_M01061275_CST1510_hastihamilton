# app/data/schema.py

from app.data.db import connect_database

def create_users_table(conn):
    """
    Create the users table if it doesn't exist.

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("Users table created successfully!")


def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,              -- optional, can stay NULL
            date TEXT,                     -- e.g., '2024-11-01'
            incident_type TEXT,            -- 'Phishing', 'Malware', etc.
            severity TEXT,                 -- 'Critical', 'High', 'Medium', 'Low'
            status TEXT,                   -- 'Open', 'Investigating', 'Resolved', 'Closed'
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("Cyber Incidents table created successfully!")


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("Datasets Metadata table created successfully!")


def create_it_tickets_table(conn):
    """
    Create the it_tickets table.

    Matches what load_it_tickets() inserts:
    (priority, status, category, subject, description, created_date, resolved_date, assigned_to)
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("IT Tickets table created successfully!")


def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
