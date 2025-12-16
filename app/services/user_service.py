import sqlite3
import bcrypt
from pathlib import Path

# Database connection helper
from app.data.db import connect_database

# User data access functions
from app.data.users import get_user_by_username, insert_user

# Schema helper (used elsewhere to create tables)
from app.data.schema import create_users_table

# Path to database file
from app.data.db import DB_PATH

# Directory that may contain legacy user data
DATA_DIR = Path("DATA")


def register_user(username, password, role='user'):
    # ------------------------------------------------------------
    # Register a new user with a hashed password
    #
    # - Hashes the plaintext password using bcrypt
    # - Inserts the user into the database
    # - Handles duplicate usernames safely
    # ------------------------------------------------------------

    # Open database connection
    conn = connect_database()

    # Hash the password using bcrypt (automatic salting)
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    try:
        # Insert user into database
        insert_user(username, password_hash, role)

        # Close connection
        conn.close()

        return True, f"User '{username}' registered successfully."

    except sqlite3.IntegrityError:
        # Triggered if username already exists (UNIQUE constraint)
        conn.close()
        return False, f"Username '{username}' already exists."


def login_user(username, password):
    # ------------------------------------------------------------
    # Authenticate a user using bcrypt password verification
    #
    # - Fetches user record by username
    # - Compares hashed password securely
    # ------------------------------------------------------------

    # Retrieve user record from database
    user = get_user_by_username(username)

    # If user does not exist
    if not user:
        return False, "User not found."

    # Extract stored password hash (3rd column)
    stored_hash = user[2]

    # Verify password against stored bcrypt hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, f"Login successful! Welcome, {username}."
    else:
        return False, "Incorrect password."


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    # ------------------------------------------------------------
    # Migrate legacy users from users.txt into SQLite database
    #
    # - Reads username + password_hash from file
    # - Inserts users safely using INSERT OR IGNORE
    # ------------------------------------------------------------

    # If legacy file does not exist, stop migration
    if not filepath.exists():
        print(f" File not found: {filepath}")
        print("   No users to migrate.")
        return

    cursor = conn.cursor()
    migrated_count = 0

    # Open legacy users file
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            parts = line.split(",")

            # Expect username,password_hash format
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    # Insert user if not already present
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO users (username, password_hash, role)
                        VALUES (?, ?, ?)
                        """,
                        (username, password_hash, "user"),
                    )

                    # Count successful migrations
                    if cursor.rowcount > 0:
                        migrated_count += 1

                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")

    # Commit all inserts
    conn.commit()

    print(f" Migrated {migrated_count} users from {filepath.name}")


def register_user(username, password, role="user"):
    # ------------------------------------------------------------
    # Register a new user (alternative implementation)
    #
    # - Checks for duplicate usernames manually
    # - Hashes password with bcrypt
    # - Inserts user into database
    # ------------------------------------------------------------

    conn = connect_database()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash password securely
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    # Insert new user record
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )

    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    # ------------------------------------------------------------
    # Authenticate a user against the database
    #
    # - Retrieves user by username
    # - Compares bcrypt password hashes
    # ------------------------------------------------------------

    conn = connect_database()
    cursor = conn.cursor()

    # Fetch user record
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()

    # User does not exist
    if not user:
        return False, "Username not found."

    # Stored password hash
    stored_hash = user[2]

    # Convert inputs to bytes for bcrypt
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

    # Verify password
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}."
    else:
        return False, "Invalid password."
