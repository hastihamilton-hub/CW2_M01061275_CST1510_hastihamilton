# Print which file is running (useful for debugging)
print("RUNNING FILE:", __file__)

import pandas as pd

# Database utilities
from app.data.db import connect_database, DATA_DIR
from app.data.schema import create_all_tables

# User authentication services
from app.services.user_service import (
    migrate_users_from_file,
    register_user,
    login_user,
)

# Cybersecurity incident services (CRUD + analytics)
from app.data.incidents import (
    insert_incident,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status,
)


# -----------------------------------------------------
# Load Cybersecurity Incidents from CSV into Database
# -----------------------------------------------------
def load_cyber_incidents(conn):
    """
    Reads cyber_incidents.csv and inserts its rows
    into the cyber_incidents database table.
    """
    csv_path = DATA_DIR / "cyber_incidents.csv"

    # Check if CSV file exists
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0

    # Load CSV into pandas DataFrame
    df = pd.read_csv(csv_path)
    print(f"Loading cyber_incidents from {csv_path} ...")
    print("cyber_incidents CSV columns:", list(df.columns))

    cursor = conn.cursor()
    count = 0

    # Insert each row into database
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO cyber_incidents
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["timestamp"],
                row["category"],
                row["severity"],
                row["status"],
                row["description"],
                None,  # reported_by left NULL for now
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows into 'cyber_incidents'.")
    return count


# -----------------------------------------------------
# Load Dataset Metadata (Data Science Domain)
# -----------------------------------------------------
def load_datasets_metadata(conn):
    """
    Loads datasets_metadata.csv into datasets_metadata table.
    Represents the Data Science domain.
    """
    csv_path = DATA_DIR / "datasets_metadata.csv"

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    print(f"Loading datasets_metadata from {csv_path} ...")
    print("datasets_metadata CSV columns:", list(df.columns))

    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO datasets_metadata
            (dataset_name, category, source, last_updated, record_count, file_size_mb)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["name"],
                None,  # category optional
                row["uploaded_by"],
                row["upload_date"],
                row["rows"],
                row["columns"],
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows into 'datasets_metadata'.")
    return count


# -----------------------------------------------------
# Load IT Support Tickets (IT Operations Domain)
# -----------------------------------------------------
def load_it_tickets(conn):
    """
    Loads it_tickets.csv into the it_tickets table.
    Represents the IT Operations domain.
    """
    csv_path = DATA_DIR / "it_tickets.csv"

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    print(f"Loading it_tickets from {csv_path} ...")
    print("it_tickets CSV columns:", list(df.columns))

    cursor = conn.cursor()
    count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO it_tickets
            (priority, status, category, subject,
             description, created_date, resolved_date, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["priority"],
                row["status"],
                None,  # category not provided
                row["description"],  # reused as subject
                row["description"],
                row["created_at"],
                None,  # resolved_date initially NULL
                row["assigned_to"],
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows into 'it_tickets'.")
    return count


# -----------------------------------------------------
# Automated Testing for Week 8 Requirements
# -----------------------------------------------------
def run_comprehensive_tests():
    """
    Runs authentication, CRUD, and analytical tests
    to verify full system functionality.
    """

    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # -------- TEST 1: Authentication --------
    print("\n[TEST 1] Authentication")
    username = "test_user"
    password = "TestPass123!"

    success, msg = register_user(username, password, "user")
    print(f"  Register: {'SUCCESS' if success else 'FAIL'} - {msg}")

    success, msg = login_user(username, password)
    print(f"  Login:    {'SUCCESS' if success else 'FAIL'} - {msg}")

    # -------- TEST 2: CRUD Operations --------
    print("\n[TEST 2] CRUD Operations")

    incident_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        username,
    )
    print(f"  Create: SUCCESS - Incident #{incident_id} created")

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(incident_id,),
    )

    print("  Read:", "SUCCESS" if not df.empty else "FAIL")

    updated = update_incident_status(conn, incident_id, "Resolved")
    print("  Update:", "SUCCESS" if updated > 0 else "FAIL")

    deleted = delete_incident(conn, incident_id)
    print("  Delete:", "SUCCESS" if deleted > 0 else "FAIL")

    # -------- TEST 3: Analytical Queries --------
    print("\n[TEST 3] Analytical Queries")

    df_type = get_incidents_by_type_count(conn)
    print(f"  Incidents by type: {len(df_type)} rows")

    df_high = get_high_severity_by_status(conn)
    print(f"  High severity incidents: {len(df_high)} rows")

    conn.close()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


# -----------------------------------------------------
# Main Execution (Week 8 Demo)
# -----------------------------------------------------
def main():
    print("=" * 60)
    print("WEEK 8 DATABASE SYSTEM DEMO")
    print("=" * 60)

    conn = connect_database()
    print("Connected to database.")

    # Create all required tables
    create_all_tables(conn)
    print("Tables created.")

    # Migrate users from legacy file
    migrate_users_from_file(conn)

    # Authentication tests
    register_user("newuser", "MyStrongPass123!", "analyst")
    print("User registration test completed.")

    print("Login test (correct pw):", login_user("newuser", "MyStrongPass123!")[1])
    print("Login test (wrong pw):", login_user("newuser", "WrongPassword")[1])

    # Load all domain datasets
    print("\nLoading CSV files...")
    load_cyber_incidents(conn)
    load_datasets_metadata(conn)
    load_it_tickets(conn)
    print("CSV loading complete.")

    conn.close()
    print("Setup complete.")

    # Run full automated test suite
    run_comprehensive_tests()


if __name__ == "__main__":
    main()
