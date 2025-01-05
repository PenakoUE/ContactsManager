import sqlite3
from structures import DoublyLinkedList


def create_database():
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT
        )
    """)
    connection.commit()
    connection.close()


def load_contacts_to_list():
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, first_name, last_name, phone_number, email FROM contacts ORDER BY last_name, first_name
    """)
    contacts = cursor.fetchall()
    connection.close()

    contact_list = DoublyLinkedList()
    for contact in contacts:
        contact_list.append(contact)

    return contact_list


def add_contact_to_db(first_name, last_name, phone_number, email):
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO contacts (first_name, last_name, phone_number, email)
        VALUES (?, ?, ?, ?)
    """, (first_name, last_name, phone_number, email))
    connection.commit()
    contact_id = cursor.lastrowid
    connection.close()
    return contact_id


def update_contact_in_db(contact_id, first_name, last_name, phone_number, email):
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE contacts
        SET first_name = ?, last_name = ?, phone_number = ?, email = ?
        WHERE id = ?
    """, (first_name, last_name, phone_number, email, contact_id))
    connection.commit()
    connection.close()


def delete_contact_from_db(contact_id):
    connection = sqlite3.connect("contacts.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    connection.commit()
    connection.close()
