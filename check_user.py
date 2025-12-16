from app.data.db import connect_database


def check_users():
    # ------------------------------------------------------------
    # Connect to the SQLite database and retrieve all users
    # ------------------------------------------------------------

    # Open database connection
    conn = connect_database()
    cursor = conn.cursor()

    # Execute query to fetch user ID, username, and role
    cursor.execute("SELECT id, username, role FROM users")

    # Retrieve all matching rows
    users = cursor.fetchall()

    # Display header
    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)

    # Print each user in a formatted row
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

    # Print total user count
    print(f"\nTotal users: {len(users)}")

    # Close database connection
    conn.close()


# ------------------------------------------------------------
# Run this script directly to list all users in the database
# ------------------------------------------------------------
if __name__ == "__main__":
    check_users()
