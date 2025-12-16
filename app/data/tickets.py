"""
tickets.py
-----------
This module handles all database operations related to the
IT Operations domain of the Multi-Domain Intelligence Platform.

It provides basic CRUD (Create, Read, Update, Delete) functions
for managing IT support tickets stored in the SQLite database.
"""

import sqlite3
from app.data.db import connect_database


def create_ticket(title, priority, status, assigned_to, description):
    """
    Create a new IT support ticket and store it in the database.

    Parameters:
    - title (str): Short title describing the issue
    - priority (str): Ticket priority (Low / Medium / High)
    - status (str): Current ticket status (Open / In Progress / Closed)
    - assigned_to (str): Person or team assigned to the ticket
    - description (str): Detailed description of the issue
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Insert a new ticket record into the it_tickets table
    cursor.execute(
        """
        INSERT INTO it_tickets (title, priority, status, assigned_to, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, priority, status, assigned_to, description),
    )

    conn.commit()
    conn.close()


def get_all_tickets():
    """
    Retrieve all IT tickets from the database.

    Returns:
    - list: A list of all ticket records
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Select all tickets
    cursor.execute("SELECT * FROM it_tickets")
    tickets = cursor.fetchall()

    conn.close()
    return tickets


def update_ticket_status(ticket_id, new_status):
    """
    Update the status of an existing IT ticket.

    Parameters:
    - ticket_id (int): ID of the ticket to update
    - new_status (str): New status value
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Update the ticket status safely using a parameterized query
    cursor.execute(
        """
        UPDATE it_tickets
        SET status = ?
        WHERE id = ?
        """,
        (new_status, ticket_id),
    )

    conn.commit()
    conn.close()


def delete_ticket(ticket_id):
    """
    Delete an IT ticket from the database.

    Parameters:
    - ticket_id (int): ID of the ticket to delete
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Remove the ticket with the specified ID
    cursor.execute(
        """
        DELETE FROM it_tickets
        WHERE id = ?
        """,
        (ticket_id,),
    )

    conn.commit()
    conn.close()
