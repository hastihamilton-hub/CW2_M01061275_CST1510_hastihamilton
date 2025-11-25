import sqlite3
import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table
from app.data.db import DB_PATH

DATA_DIR = Path("DATA")


def register_user(username, password, role='user'):
    """Register new user with hashed password."""
    conn = connect_database()

    # Hash the password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    try:
        insert_user(username, password_hash, role)
        conn.close()
        return True, f"User '{username}' registered successfully."
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"Username '{username}' already exists."



def login_user(username, password):
    """Log in a user by verifying password hash."""
    user = get_user_by_username(username)

    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful! Welcome, {username}."
    else:
        return False, "Incorrect password."

def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    """Migrate users from users.txt to the SQLite database."""

    if not filepath.exists():
        print(f" File not found: {filepath}")
        print("   No users to migrate.")
        return

    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")

            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO users (username, password_hash, role)
                        VALUES (?, ?, ?)
                        """,
                        (username, password_hash, "user"),
                    )

                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    conn.commit()
    print(f" Migrated {migrated_count} users from {filepath.name}")

def register_user(username, password, role="user"):
    """
    Register a new user in the database.

    Args:
        username: User's login name
        password: Plain text password (will be hashed)
        role: User role (default: 'user')

    Returns:
        tuple: (success, message)
    """
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"

def login_user(username, password):
    """
    Authenticate a user against the database.

    Args:
        username: User's login name
        password: Plain text password to verify

    Returns:
        tuple: (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."

    stored_hash = user[2]

    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."

