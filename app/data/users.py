# app/data/users.py

import sqlite3
from app.data.db import connect_database

def get_user_by_username(username: str):
    """Return user row by username or None."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(username: str, password_hash: str, role: str = "user"):
    """Insert a new user into the database."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, role)
    )

    conn.commit()
    conn.close()
