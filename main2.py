print("RUNNING FILE:", __file__)

import pandas as pd

from app.data.db import connect_database, DATA_DIR
from app.data.schema import create_all_tables

from app.services.user_service import (
    migrate_users_from_file,
    register_user,
    login_user,
)

from app.data.incidents import (
    insert_incident,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status,
)


def load_cyber_incidents(conn):
    """
    Load cyber_incidents.csv into the cyber_incidents table.
    """
    csv_path = DATA_DIR / "cyber_incidents.csv"

    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    print(f"Loading cyber_incidents from {csv_path} ...")
    print("cyber_incidents CSV columns:", list(df.columns))

    cursor = conn.cursor()
    count = 0

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
                None,
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows from cyber_incidents.csv into 'cyber_incidents'.")
    return count


def load_datasets_metadata(conn):
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
                None,
                row["uploaded_by"],
                row["upload_date"],
                row["rows"],
                row["columns"],
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows from datasets_metadata.csv into 'datasets_metadata'.")
    return count


def load_it_tickets(conn):
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
                None,
                row["description"],
                row["description"],
                row["created_at"],
                None,
                row["assigned_to"],
            ),
        )
        count += 1

    conn.commit()
    print(f"Loaded {count} rows from it_tickets.csv into 'it_tickets'.")
    return count


def run_comprehensive_tests():
    """
    Step 10.1 – Comprehensive Database Test
    """

    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # TEST 1 – Authentication
    print("\n[TEST 1] Authentication")
    username = "test_user"
    password = "TestPass123!"

    success, msg = register_user(username, password, "user")
    print(f"  Register: {'SUCCESS' if success else 'FAIL'} - {msg}")

    success, msg = login_user(username, password)
    print(f"  Login:    {'SUCCESS' if success else 'FAIL'} - {msg}")

    # TEST 2 – CRUD Operations
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
    if df.empty:
        print(f"  Read:   FAIL - Incident not found")
    else:
        print(f"  Read:   SUCCESS - Found incident #{incident_id}")

    updated = update_incident_status(conn, incident_id, "Resolved")
    if updated > 0:
        print("  Update: SUCCESS - Status updated")
    else:
        print("  Update: FAIL")

    deleted = delete_incident(conn, incident_id)
    if deleted > 0:
        print("  Delete: SUCCESS - Incident deleted")
    else:
        print("  Delete: FAIL")

    # TEST 3 – Analytical SQL Queries
    print("\n[TEST 3] Analytical Queries")

    df_type = get_incidents_by_type_count(conn)
    print(f"  By Type: {len(df_type)} rows returned")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: {len(df_high)} rows returned")

    conn.close()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


def main():
    print("=" * 60)
    print("WEEK 8 DATABASE SYSTEM DEMO")
    print("=" * 60)

    conn = connect_database()
    print("Connected to database.")

    create_all_tables(conn)
    print("Tables created.")

    migrate_users_from_file(conn)

    success, msg = register_user("newuser", "MyStrongPass123!", "analyst")
    print(msg)

    success, msg = login_user("newuser", "MyStrongPass123!")
    print("Login test (correct pw):", msg)

    success, msg = login_user("newuser", "WrongPassword")
    print("Login test (wrong pw):", msg)

    print("\nLoading CSV files...")
    load_cyber_incidents(conn)
    load_datasets_metadata(conn)
    load_it_tickets(conn)
    print("CSV loading complete.")

    conn.close()
    print("Setup complete.")

    run_comprehensive_tests()


if __name__ == "__main__":
    main()
