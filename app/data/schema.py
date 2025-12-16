from app.data.db import connect_database


def create_users_table(conn):
    # Create the users table to store authentication and role information
    # This table supports login, registration, and role-based access
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- unique user ID
            username TEXT NOT NULL UNIQUE,          -- unique username
            password_hash TEXT NOT NULL,            -- bcrypt-hashed password
            role TEXT DEFAULT 'user',                -- user role (user/admin)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- account creation time
        )
    """)

    conn.commit()  # Save table creation
    print("Users table created successfully!")


def create_cyber_incidents_table(conn):
    # Create table for the Cybersecurity domain
    # Stores security incidents loaded from CSV or added manually
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- internal database ID
            incident_id TEXT,                       -- optional external incident ID
            date TEXT,                              -- incident date/time
            incident_type TEXT,                     -- type/category of incident
            severity TEXT,                          -- severity level (Low/Medium/High)
            status TEXT,                            -- current incident status
            description TEXT,                       -- detailed description
            reported_by TEXT,                       -- person/system that reported it
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- record creation time
        )
    """)

    conn.commit()
    print("Cyber Incidents table created successfully!")


def create_datasets_metadata_table(conn):
    # Create table for the Data Science domain
    # Stores metadata about datasets used in the platform
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- internal dataset ID
            dataset_name TEXT NOT NULL,              -- dataset name
            category TEXT,                           -- dataset category (optional)
            source TEXT,                             -- data source or uploader
            last_updated TEXT,                       -- last update date
            record_count INTEGER,                    -- number of records
            file_size_mb REAL,                       -- approximate dataset size
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- metadata creation time
        )
    """)

    conn.commit()
    print("Datasets Metadata table created successfully!")


def create_it_tickets_table(conn):
    # Create table for the IT Operations domain
    # Stores helpdesk and support tickets
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- internal ticket ID
            priority TEXT,                           -- ticket priority
            status TEXT,                             -- open / in-progress / closed
            category TEXT,                           -- ticket category (optional)
            subject TEXT,                            -- short ticket subject
            description TEXT,                        -- detailed issue description
            created_date TEXT,                       -- ticket creation date
            resolved_date TEXT,                      -- resolution date (if closed)
            assigned_to TEXT                         -- support staff assigned
        )
    """)

    conn.commit()
    print("IT Tickets table created successfully!")


def create_all_tables(conn):
    # Create all database tables required by the platform
    # This function is called once during setup
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
