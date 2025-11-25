# app/services/incidents.py

import pandas as pd


def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    CREATE: Insert a new cyber incident into the database.

    Args:
        conn: Database connection
        date (str): Incident date (YYYY-MM-DD)
        incident_type (str): Type of incident
        severity (str): Severity level
        status (str): Current status
        description (str): Incident description
        reported_by (str | None): Username of reporter (optional)

    Returns:
        int: ID of the inserted incident (primary key 'id')
    """
    cursor = conn.cursor()

    sql = """
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(sql, (
        date,
        incident_type,
        severity,
        status,
        description,
        reported_by
    ))

    conn.commit()
    return cursor.lastrowid


def get_all_incidents(conn):
    """
    READ: Retrieve all incidents from the database.

    Args:
        conn: Database connection

    Returns:
        pandas.DataFrame: All rows from the cyber_incidents table.
    """
    return pd.read_sql_query(
        "SELECT * FROM cyber_incidents",
        conn
    )


def update_incident_status(conn, incident_id, new_status):
    """
    UPDATE: Change the status of an incident.

    Args:
        conn: Database connection
        incident_id (int): The 'id' of the incident row
        new_status (str): New status value

    Returns:
        int: Number of rows updated (0 or 1)
    """
    cursor = conn.cursor()

    sql = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """

    cursor.execute(sql, (new_status, incident_id))
    conn.commit()

    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    DELETE: Remove an incident from the database.

    WARNING: This is permanent.

    Args:
        conn: Database connection
        incident_id (int): The 'id' of the incident row to delete

    Returns:
        int: Number of rows deleted (0 or 1)
    """
    cursor = conn.cursor()

    sql = """
        DELETE FROM cyber_incidents
        WHERE id = ?
    """

    cursor.execute(sql, (incident_id,))
    conn.commit()

    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.

    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """
    Count HIGH severity incidents by status.

    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) AS count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.

    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))
