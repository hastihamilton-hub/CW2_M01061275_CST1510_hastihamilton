import pandas as pd


def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    CREATE: Insert a new cyber incident into the database.
    """
    # Create a database cursor to execute SQL commands
    cursor = conn.cursor()

    # SQL statement to insert a new incident record
    sql = """
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    # Execute the SQL statement with parameterized values
    # This prevents SQL injection attacks
    cursor.execute(sql, (
        date,
        incident_type,
        severity,
        status,
        description,
        reported_by
    ))

    # Save changes to the database
    conn.commit()

    # Return the ID of the newly inserted incident
    return cursor.lastrowid


def get_all_incidents(conn):
    """
    READ: Retrieve all incidents from the database.
    """
    # Use pandas to read the entire cyber_incidents table into a DataFrame
    return pd.read_sql_query(
        "SELECT * FROM cyber_incidents",
        conn
    )


def update_incident_status(conn, incident_id, new_status):
    """
    UPDATE: Change the status of an incident.
    """
    # Create a cursor for executing the update query
    cursor = conn.cursor()

    # SQL statement to update the status of a specific incident
    sql = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """

    # Execute update using parameterized values
    cursor.execute(sql, (new_status, incident_id))

    # Commit the update to the database
    conn.commit()

    # Return the number of rows updated (0 or 1)
    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    DELETE: Remove an incident from the database.
    WARNING: This is permanent.
    """
    # Create a cursor for deletion
    cursor = conn.cursor()

    # SQL statement to delete an incident by ID
    sql = """
        DELETE FROM cyber_incidents
        WHERE id = ?
    """

    # Execute deletion safely using parameters
    cursor.execute(sql, (incident_id,))

    # Commit deletion to the database
    conn.commit()

    # Return the number of rows deleted
    return cursor.rowcount


def get_incidents_by_type_count(conn):
    """
    ANALYSIS: Count incidents grouped by incident type.
    """
    # SQL query to group incidents by type and count them
    query = """
    SELECT incident_type, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """

    # Return the aggregated results as a pandas DataFrame
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """
    ANALYSIS: Count HIGH severity incidents grouped by status.
    """
    # SQL query filtering only high-severity incidents
    query = """
    SELECT status, COUNT(*) AS count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """

    # Return grouped results as a DataFrame
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """
    ANALYSIS: Find incident types with more than a specified number of cases.
    """
    # SQL query using HAVING to filter groups by count
    query = """
    SELECT incident_type, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """

    # Execute query with parameter for minimum count
    return pd.read_sql_query(query, conn, params=(min_count,))
