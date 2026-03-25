import psycopg2
import csv
from config import load_config
from connect import connect

# --- Connection ---

config = load_config()
conn = connect()


# --- Table setup ---

def create_table():
    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    with conn.cursor() as cur:
        cur.execute(command)
        conn.commit()


# --- INSERT ---

def insert_contact(username, phone):
    command = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    """
    with conn.cursor() as cur:
        cur.execute(command, (username, phone))
        conn.commit()


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    try:
        insert_contact(username, phone)
        print(f"Added: {username} - {phone}")
    except Exception as e:
        print("Error:", e)


def insert_from_csv(csv_file):
    command = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO NOTHING
    """

    try:
        with conn.cursor() as cur:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    username, phone = row
                    cur.execute(command, (username, phone))

            conn.commit()
        print(f"Imported contacts from {csv_file}")

    except Exception as e:
        print("Error:", e)


# --- SELECT ---

def get_all_contacts():
    command = "SELECT * FROM phonebook ORDER BY username"
    with conn.cursor() as cur:
        cur.execute(command)
        return cur.fetchall()


def search_contacts(pattern):
    command = """
    SELECT * FROM phonebook
    WHERE username ILIKE %s OR phone ILIKE %s
    """
    like_pattern = f"%{pattern}%"
    with conn.cursor() as cur:
        cur.execute(command, (like_pattern, like_pattern))
        return cur.fetchall()


# --- UPDATE ---

def update_phone_by_username(username, new_phone):
    command = """
    UPDATE phonebook
    SET phone = %s
    WHERE username = %s
    """
    with conn.cursor() as cur:
        cur.execute(command, (new_phone, username))
        conn.commit()

        if cur.rowcount == 0:
            print("User not found.")
        else:
            print(f"Updated {cur.rowcount} row(s)")


def update_username_by_phone(phone, new_username):
    command = """
    UPDATE phonebook
    SET username = %s
    WHERE phone = %s
    """
    with conn.cursor() as cur:
        cur.execute(command, (new_username, phone))
        conn.commit()

        if cur.rowcount == 0:
            print("Phone not found.")
        else:
            print(f"Updated {cur.rowcount} row(s)")


# --- DELETE ---

def delete_by_username(username):
    command = "DELETE FROM phonebook WHERE username = %s"
    with conn.cursor() as cur:
        cur.execute(command, (username,))
        conn.commit()

        if cur.rowcount == 0:
            print("User not found.")
        else:
            print(f"Deleted {cur.rowcount} row(s)")


def delete_by_phone(phone):
    command = "DELETE FROM phonebook WHERE phone = %s"
    with conn.cursor() as cur:
        cur.execute(command, (phone,))
        conn.commit()

        if cur.rowcount == 0:
            print("Phone not found.")
        else:
            print(f"Deleted {cur.rowcount} row(s)")


# --- Print helper ---

def print_contacts(contacts):
    if not contacts:
        print("(no contacts)")
        return

    for c in contacts:
        print(f"[{c[0]}] {c[1]} - {c[2]}")


# --- Main menu ---

def main():

    create_table()

    while True:
        print("\n--- PhoneBook ---")
        print("1. Show all contacts")
        print("2. Add contact (console)")
        print("3. Import from CSV")
        print("4. Search")
        print("5. Update phone by username")
        print("6. Update username by phone")
        print("7. Delete by username")
        print("8. Delete by phone")
        print("0. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            print_contacts(get_all_contacts())

        elif choice == "2":
            insert_from_console()

        elif choice == "3":
            filename = input("CSV file path: ")
            insert_from_csv(filename)

        elif choice == "4":
            pattern = input("Search: ")
            print_contacts(search_contacts(pattern))

        elif choice == "5":
            username = input("Username: ")
            new_phone = input("New phone: ")
            update_phone_by_username(username, new_phone)

        elif choice == "6":
            phone = input("Phone: ")
            new_username = input("New username: ")
            update_username_by_phone(phone, new_username)

        elif choice == "7":
            username = input("Username: ")
            delete_by_username(username)

        elif choice == "8":
            phone = input("Phone: ")
            delete_by_phone(phone)

        elif choice == "0":
            break

        else:
            print("Invalid choice")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()