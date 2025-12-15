# app/data/schema.py

from app.data.db import connect_database


def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("Users table created successfully!")


def create_cyber_incidents_table(conn):
    """
    Create cyber_incidents table matching load_cyber_incidents().
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,              -- optional CSV column
            date TEXT,                     -- CSV: timestamp
            incident_type TEXT,            -- CSV: category
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("Cyber Incidents table created successfully!")


def create_datasets_metadata_table(conn):
    """
    Create datasets_metadata table matching load_datasets_metadata().
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,   -- CSV: name
            category TEXT,                -- no column in CSV → NULL
            source TEXT,                  -- CSV: uploaded_by
            last_updated TEXT,            -- CSV: upload_date
            record_count INTEGER,         -- CSV: rows
            file_size_mb REAL,            -- CSV: columns (we reuse)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("Datasets Metadata table created successfully!")


def create_it_tickets_table(conn):
    """
    Create it_tickets table matching load_it_tickets().
    IMPORTANT: DO NOT include ticket_id — your loader does NOT insert it.
    """
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            priority TEXT,
            status TEXT,
            category TEXT,        -- will be NULL
            subject TEXT,         -- we use description as subject
            description TEXT,
            created_date TEXT,    -- CSV: created_at
            resolved_date TEXT,
            assigned_to TEXT
        )
    """)

    conn.commit()
    print("IT Tickets table created successfully!")


def create_all_tables(conn):
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
