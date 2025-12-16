import sqlite3
from app.data.db import connect_database


def get_user_by_username(username: str):
    """
    Retrieve a user record from the database by username.

    Parameters:
    - username (str): The username to search for

    Returns:
    - tuple containing user fields (id, username, password_hash, role, created_at)
      or None if the user does not exist.
    """
    # Open database connection
    conn = connect_database()
    cursor = conn.cursor()

    # Parameterized query to prevent SQL injection
    cursor.execute(
        """
        SELECT id, username, password_hash, role, created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    # Fetch a single matching row
    user = cursor.fetchone()

    # Close database connection
    conn.close()

    return user


def insert_user(username: str, password_hash: str, role: str = "user"):
    """
    Insert a new user into the users table.

    Parameters:
    - username (str): Chosen username
    - password_hash (str): Securely hashed password (bcrypt)
    - role (str): User role (default = "user")

    This function assumes that username uniqueness has already been validated.
    """
    # Open database connection
    conn = connect_database()
    cursor = conn.cursor()

    # Insert user using a parameterized query for security
    cursor.execute(
        """
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, role)
    )

    # Save changes to database
    conn.commit()

    # Close database connection
    conn.close()
