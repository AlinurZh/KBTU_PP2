import json
import csv
from connect import connect


def print_rows(rows):
    # Небольшая функция, чтобы одинаково красиво выводить результаты запросов
    if not rows:
        print("  (no results)")
    else:
        for row in rows:
            print(" ", row)


def setup_schema():
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            with open("schema.sql", "r", encoding="utf-8") as f:
                cur.execute(f.read())

        conn.commit()
        print("Schema ready.")

    except Exception as e:
        print("Error setting up schema:", e)

    finally:
        conn.close()


def run_sql_file(filename):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            with open(filename, "r", encoding="utf-8") as f:
                cur.execute(f.read())

        conn.commit()
        print(f"{filename} loaded.")

    except Exception as e:
        print(f"Error loading {filename}:", e)

    finally:
        conn.close()


def add_contact(username, email=None, birthday=None, group_name=None):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            group_id = None

            # Если пользователь указал группу, сначала ищем её id в таблице groups
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                row = cur.fetchone()

                if row:
                    group_id = row[0]
                else:
                    print(f"Group '{group_name}' not found. Setting group to NULL.")

            cur.execute("""
                INSERT INTO contacts (username, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (username) DO NOTHING
            """, (username, email, birthday, group_id))

        conn.commit()
        print(f"Contact '{username}' added.")

    except Exception as e:
        conn.rollback()
        print("Error adding contact:", e)

    finally:
        conn.close()


def add_phone(contact_name, phone, phone_type):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # Номер добавляется через процедуру из procedures.sql
            cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))

        conn.commit()
        print(f"Phone added to '{contact_name}'.")

    except Exception as e:
        conn.rollback()
        print("Error adding phone:", e)

    finally:
        conn.close()


def move_to_group(contact_name, group_name):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # Перемещение контакта в группу тоже сделано через SQL-процедуру
            cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))

        conn.commit()
        print(f"'{contact_name}' moved to group '{group_name}'.")

    except Exception as e:
        conn.rollback()
        print("Error moving to group:", e)

    finally:
        conn.close()


def search_contacts(query):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

        print(f"\nSearch results for '{query}':")
        print_rows(rows)

    except Exception as e:
        print("Error searching:", e)

    finally:
        conn.close()


def filter_by_group(group_name):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                WHERE g.name ILIKE %s
                ORDER BY c.username
            """, (group_name,))

            rows = cur.fetchall()

        print(f"\nContacts in group '{group_name}':")
        print_rows(rows)

    except Exception as e:
        print("Error filtering by group:", e)

    finally:
        conn.close()


def search_by_email(email_pattern):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, birthday
                FROM contacts
                WHERE email ILIKE %s
            """, (f"%{email_pattern}%",))

            rows = cur.fetchall()

        print(f"\nContacts matching email '{email_pattern}':")
        print_rows(rows)

    except Exception as e:
        print("Error searching by email:", e)

    finally:
        conn.close()


def show_all_contacts(sort_by="username"):
    allowed = {"username", "birthday", "created_at"}

    # Защита от неправильного поля сортировки
    if sort_by not in allowed:
        sort_by = "username"

    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.id, c.username, c.email, c.birthday, g.name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.{sort_by}
            """)

            rows = cur.fetchall()

        print(f"\nAll contacts (sorted by {sort_by}):")
        print_rows(rows)

    except Exception as e:
        print("Error showing contacts:", e)

    finally:
        conn.close()


def paginated_navigation():
    limit = 3
    offset = 0

    while True:
        conn = connect()
        if not conn:
            return

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
                rows = cur.fetchall()

        except Exception as e:
            print("Error:", e)
            conn.close()
            return

        finally:
            conn.close()

        print(f"\n--- Page (offset={offset}) ---")

        if not rows:
            print("  No more contacts.")
        else:
            print_rows(rows)

        print("  [n] Next  [p] Prev  [q] Quit")
        choice = input("  Choice: ").strip().lower()

        if choice == "n":
            if rows:
                offset += limit
            else:
                print("  Already at last page.")

        elif choice == "p":
            offset = max(0, offset - limit)

        elif choice == "q":
            break


def delete_contact(username):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

            if cur.rowcount == 0:
                print("Contact not found.")
            else:
                print(f"Contact '{username}' deleted.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error deleting:", e)

    finally:
        conn.close()


def export_to_json(filename="contacts.json"):
    conn = connect()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.username, c.email, c.birthday::TEXT, g.name as grp
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
            """)

            contacts = cur.fetchall()
            result = []

            for (username, email, birthday, grp) in contacts:
                # Для каждого контакта отдельно достаём его номера телефонов
                cur.execute("""
                    SELECT p.phone, p.type
                    FROM phones p
                    JOIN contacts c ON c.id = p.contact_id
                    WHERE c.username = %s
                """, (username,))

                phones = [{"phone": ph, "type": tp} for ph, tp in cur.fetchall()]

                result.append({
                    "username": username,
                    "email": email,
                    "birthday": birthday,
                    "group": grp,
                    "phones": phones
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"Exported {len(result)} contacts to '{filename}'.")

    except Exception as e:
        print("Error exporting:", e)

    finally:
        conn.close()


def import_from_json(filename="contacts.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

    except Exception as e:
        print("Error reading file:", e)
        return

    conn = connect()
    if not conn:
        return

    try:
        for item in data:
            username = item.get("username")
            email = item.get("email")
            birthday = item.get("birthday")
            grp = item.get("group")
            phones = item.get("phones", [])

            with conn.cursor() as cur:
                # Если контакт уже есть, спрашиваем, нужно ли его заменить
                cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
                existing = cur.fetchone()

                if existing:
                    choice = input(f"Contact '{username}' already exists. Overwrite? (y/n): ").strip().lower()

                    if choice != "y":
                        print(f"  Skipped '{username}'.")
                        continue
                    else:
                        cur.execute("DELETE FROM contacts WHERE username = %s", (username,))

                group_id = None

                if grp:
                    cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                    row = cur.fetchone()

                    if row:
                        group_id = row[0]

                cur.execute("""
                    INSERT INTO contacts (username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (username, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                # После добавления контакта записываем все его номера
                for p in phones:
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                    """, (contact_id, p.get("phone"), p.get("type")))

            conn.commit()
            print(f"  Imported '{username}'.")

    except Exception as e:
        conn.rollback()
        print("Error importing:", e)

    finally:
        conn.close()


def import_from_csv(filename="contacts.csv"):
    """
    Expected CSV columns:
    username, email, birthday, group, phone, phone_type
    """

    conn = connect()
    if not conn:
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            with conn.cursor() as cur:
                for row in reader:
                    username = row.get("username", "").strip()
                    email = row.get("email", "").strip() or None
                    birthday = row.get("birthday", "").strip() or None
                    grp = row.get("group", "").strip() or None
                    phone = row.get("phone", "").strip() or None
                    phone_type = row.get("phone_type", "mobile").strip()

                    if not username:
                        continue

                    group_id = None

                    if grp:
                        cur.execute("SELECT id FROM groups WHERE name = %s", (grp,))
                        r = cur.fetchone()

                        if r:
                            group_id = r[0]

                    # Если контакт уже есть, обновляем его данные
                    cur.execute("""
                        INSERT INTO contacts (username, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (username) 
                        DO UPDATE SET email = EXCLUDED.email,
                                    birthday = EXCLUDED.birthday,
                                    group_id = EXCLUDED.group_id
                        RETURNING id
                    """, (username, email, birthday, group_id))

                    contact_id = cur.fetchone()[0]

                    if phone:
                        cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                        """, (contact_id, phone, phone_type))

            conn.commit()

        print(f"CSV '{filename}' imported successfully.")

    except Exception as e:
        conn.rollback()
        print("Error importing CSV:", e)

    finally:
        conn.close()


def menu():
    print("Initializing...")
    setup_schema()
    run_sql_file("procedures.sql")

    while True:
        print("\n===== PHONEBOOK =====")
        print("1.  Add contact")
        print("2.  Add phone to contact")
        print("3.  Move contact to group")
        print("4.  Search (name / email / phone)")
        print("5.  Filter by group")
        print("6.  Search by email")
        print("7.  Show all contacts")
        print("8.  Browse pages")
        print("9.  Delete contact")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Import from CSV")
        print("0.  Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            email = input("Email (optional): ").strip() or None
            birthday = input("Birthday YYYY-MM-DD (optional): ").strip() or None
            group_name = input("Group (Family/Work/Friend/Other): ").strip() or None
            add_contact(username, email, birthday, group_name)

        elif choice == "2":
            name = input("Contact username: ").strip()
            phone = input("Phone: ").strip()
            ptype = input("Type (home/work/mobile): ").strip()
            add_phone(name, phone, ptype)

        elif choice == "3":
            name = input("Contact username: ").strip()
            group = input("Group name: ").strip()
            move_to_group(name, group)

        elif choice == "4":
            query = input("Search query: ").strip()
            search_contacts(query)

        elif choice == "5":
            group = input("Group name: ").strip()
            filter_by_group(group)

        elif choice == "6":
            pattern = input("Email pattern: ").strip()
            search_by_email(pattern)

        elif choice == "7":
            print("Sort by: 1) username  2) birthday  3) created_at")
            s = input("Choice: ").strip()
            sort_map = {"1": "username", "2": "birthday", "3": "created_at"}
            sort_by = sort_map.get(s, "username")
            show_all_contacts(sort_by)

        elif choice == "8":
            paginated_navigation()

        elif choice == "9":
            username = input("Username to delete: ").strip()
            delete_contact(username)

        elif choice == "10":
            fname = input("Output file (default: contacts.json): ").strip() or "contacts.json"
            export_to_json(fname)

        elif choice == "11":
            fname = input("Input file (default: contacts.json): ").strip() or "contacts.json"
            import_from_json(fname)

        elif choice == "12":
            fname = input("CSV file (default: contacts.csv): ").strip() or "contacts.csv"
            import_from_csv(fname)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()