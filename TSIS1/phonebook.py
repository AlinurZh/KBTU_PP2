"""
TSIS 1 – PhoneBook Extended
Builds on Practice 7 & 8
"""

import csv
import json
import os
import re
from datetime import date, datetime

import psycopg2
from connect import connect


# ── Phone validation ──────────────────────────────────────────────────────────

def is_valid_kz_phone(phone: str) -> bool:
    if not phone:
        return False
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return bool(re.fullmatch(r'^(\+7|7|8)\d{10}$', cleaned))


def normalize_phone(phone: str) -> str:
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    if cleaned.startswith('+7'):
        return cleaned
    elif cleaned.startswith('8'):
        return '+7' + cleaned[1:]
    else:
        return '+' + cleaned


def input_phone(prompt: str = "Phone (+7XXXXXXXXXX): ") -> str | None:
    attempts = 3
    while attempts > 0:
        phone = input(prompt).strip()
        if is_valid_kz_phone(phone):
            normalized = normalize_phone(phone)
            if normalized != phone:
                print(f"  Normalized to: {normalized}")
            return normalized
        attempts -= 1
        print(f"  Invalid KZ phone: '{phone}'")
        print(f"  Valid formats: +77001112233 | 77001112233 | 87001112233")
        if attempts > 0:
            print(f"  Attempts left: {attempts}")
        else:
            print("  Too many invalid attempts. Operation cancelled.")
    return None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _date_serial(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def _run_sql_file(path: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()
        cur.execute(sql)
        conn.commit()
        print(f"[OK] Executed {path}")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] {path}: {e}")
    finally:
        cur.close()
        conn.close()


def _resolve_group_id(cur, group_name: str) -> int | None:
    if not group_name:
        return None
    cur.execute("SELECT id FROM groups WHERE name ILIKE %s LIMIT 1;", (group_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,))
    return cur.fetchone()[0]


def _print_full_rows(rows):
    if not rows:
        print("No records.")
        return

    headers = ["ID", "Name", "Phone", "Email", "Birthday", "Group"]

    str_rows = []
    for row in rows:
        str_rows.append([str(val) if val is not None else "" for val in row])

    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for str_row in str_rows:
            if i < len(str_row):
                max_width = max(max_width, len(str_row[i]))
        col_widths.append(max_width + 2)

    fmt = "".join(f"{{:<{w}}}" for w in col_widths)
    print(fmt.format(*headers))
    print("-" * sum(col_widths))
    for str_row in str_rows:
        while len(str_row) < len(headers):
            str_row.append("")
        print(fmt.format(*str_row))


def _pick_sort() -> str:
    print("  Sort by: (1) Name  (2) Birthday  (3) Date added")
    s = input("  Choice [1]: ").strip()
    return {"1": "name", "2": "birthday", "3": "date"}.get(s, "name")


# ── Schema init ───────────────────────────────────────────────────────────────

def init_schema():
    base = os.path.dirname(__file__)
    _run_sql_file(os.path.join(base, "schema.sql"))
    _run_sql_file(os.path.join(base, "procedures.sql"))


# ── Practice 8 wrappers (not re-implemented) ─────────────────────────────────

def search_contacts(pattern: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        rows = cur.fetchall()
        print("\nSearch results:")
        if rows:
            _print_full_rows(rows)
        else:
            print("No matching records found.")
    except Exception as e:
        print("Error in search_contacts:", e)
    finally:
        cur.close()
        conn.close()


def upsert_user(username: str, phone: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_user(%s, %s);", (username, phone))
        conn.commit()
        print(f"  User '{username}' inserted/updated successfully!")
    except Exception as e:
        conn.rollback()
        print("Error in upsert_user:", e)
    finally:
        cur.close()
        conn.close()


def insert_many_users(usernames: list, phones: list):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_many_users(%s, %s);", (usernames, phones))
        conn.commit()
        print("Bulk insert completed!")
    except Exception as e:
        conn.rollback()
        print("Error in insert_many_users:", e)
    finally:
        cur.close()
        conn.close()


def delete_user_by_username(username: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_user(%s, %s);", (username, None))
        conn.commit()
        print(f"  User '{username}' deleted.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_user_by_phone(phone: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_user(%s, %s);", (None, phone))
        conn.commit()
        print(f"  User with phone '{phone}' deleted.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


# ── Search & filter ───────────────────────────────────────────────────────────

def filter_by_group(group_name: str, sort_by: str = "name"):
    valid_sorts = {"name": "pb.username", "birthday": "pb.birthday", "date": "pb.id"}
    order_col = valid_sorts.get(sort_by, "pb.username")

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT DISTINCT pb.id, pb.username, pb.phone, pb.email,
                            pb.birthday, g.name
            FROM phonebook pb
            LEFT JOIN groups g  ON g.id = pb.group_id
            LEFT JOIN phones ph ON ph.contact_id = pb.id
            WHERE g.name ILIKE %s
            ORDER BY {order_col};
        """, (group_name,))
        rows = cur.fetchall()
        print(f"\nContacts in group '{group_name}':")
        _print_full_rows(rows) if rows else print("No contacts found.")
    except Exception as e:
        print("Error in filter_by_group:", e)
    finally:
        cur.close()
        conn.close()


def search_by_email(partial_email: str, sort_by: str = "name"):
    valid_sorts = {"name": "pb.username", "birthday": "pb.birthday", "date": "pb.id"}
    order_col = valid_sorts.get(sort_by, "pb.username")

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT pb.id, pb.username, pb.phone, pb.email,
                   pb.birthday, g.name
            FROM phonebook pb
            LEFT JOIN groups g ON g.id = pb.group_id
            WHERE pb.email ILIKE %s
            ORDER BY {order_col};
        """, (f"%{partial_email}%",))
        rows = cur.fetchall()
        print(f"\nContacts matching email '{partial_email}':")
        _print_full_rows(rows) if rows else print("No contacts found.")
    except Exception as e:
        print("Error in search_by_email:", e)
    finally:
        cur.close()
        conn.close()


def show_all_sorted(sort_by: str = "name"):
    valid_sorts = {"name": "pb.username", "birthday": "pb.birthday", "date": "pb.id"}
    order_col = valid_sorts.get(sort_by, "pb.username")

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT pb.id, pb.username, pb.phone, pb.email,
                   pb.birthday, g.name
            FROM phonebook pb
            LEFT JOIN groups g ON g.id = pb.group_id
            ORDER BY {order_col};
        """)
        rows = cur.fetchall()
        print(f"\nAll contacts (sorted by {sort_by}):")
        _print_full_rows(rows) if rows else print("Phonebook is empty.")
    except Exception as e:
        print("Error in show_all_sorted:", e)
    finally:
        cur.close()
        conn.close()


# ── Pagination ────────────────────────────────────────────────────────────────

def _fetch_page(limit: int, offset: int) -> list:
    conn = connect()
    if conn is None:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        return cur.fetchall()
    except Exception as e:
        print("Error fetching page:", e)
        return []
    finally:
        cur.close()
        conn.close()


def paginated_navigation(page_size: int = 5):
    offset = 0
    page = 1
    while True:
        rows = _fetch_page(page_size, offset)
        print(f"\n--- Page {page} ---")
        if rows:
            for row in rows:
                print(row)
        else:
            print("(no records on this page)")

        has_next = len(rows) == page_size
        has_prev = offset > 0

        options = []
        if has_next:
            options.append("next")
        if has_prev:
            options.append("prev")
        options.append("quit")

        print(f"Options: {' | '.join(options)}")
        cmd = input(">> ").strip().lower()

        if cmd == "next" and has_next:
            offset += page_size
            page += 1
        elif cmd == "prev" and has_prev:
            offset -= page_size
            page -= 1
        elif cmd == "quit":
            break
        else:
            print("Invalid option or boundary reached.")


# ── JSON export ───────────────────────────────────────────────────────────────

def export_to_json(filepath: str = "contacts_export.json"):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT pb.id, pb.username, pb.phone,
                   pb.email, pb.birthday, g.name
            FROM phonebook pb
            LEFT JOIN groups g ON g.id = pb.group_id
            ORDER BY pb.id;
        """)
        contacts = cur.fetchall()

        result = []
        for cid, username, main_phone, email, birthday, grp in contacts:
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (cid,))
            extra_phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
            result.append({
                "id": cid,
                "username": username,
                "main_phone": main_phone,
                "email": email,
                "birthday": birthday,
                "group": grp,
                "extra_phones": extra_phones,
            })

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=_date_serial, ensure_ascii=False)

        print(f"Exported {len(result)} contacts to '{filepath}'.")
    except Exception as e:
        print("Error in export_to_json:", e)
    finally:
        cur.close()
        conn.close()


# ── JSON import ───────────────────────────────────────────────────────────────

def import_from_json(filepath: str = "contacts_export.json"):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
            return

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    inserted = skipped = overwritten = 0

    try:
        for contact in data:
            username     = contact.get("username", "").strip()
            main_phone   = contact.get("main_phone", "")
            email        = contact.get("email")
            birthday     = contact.get("birthday")
            group_name   = contact.get("group")
            extra_phones = contact.get("extra_phones", [])

            if not username:
                print("  Skipping entry with no username.")
                skipped += 1
                continue

            # Validate main phone
            if not is_valid_kz_phone(main_phone):
                print(f"  Skipping '{username}': invalid phone '{main_phone}'")
                skipped += 1
                continue
            main_phone = normalize_phone(main_phone)

            # Validate extra phones
            valid_extra = []
            for ph in extra_phones:
                num = ph.get("phone", "")
                if is_valid_kz_phone(num):
                    valid_extra.append({"phone": normalize_phone(num), "type": ph.get("type", "mobile")})
                else:
                    print(f"  Skipping invalid extra phone '{num}' for '{username}'")
            extra_phones = valid_extra

            cur.execute(
                "SELECT id FROM phonebook WHERE username ILIKE %s LIMIT 1;",
                (username,)
            )
            existing = cur.fetchone()

            if existing:
                print(f"\n  Duplicate found: '{username}'")
                choice = input("  (s)kip or (o)verwrite? ").strip().lower()
                if choice != "o":
                    skipped += 1
                    continue

                group_id = _resolve_group_id(cur, group_name)
                cur.execute("""
                    UPDATE phonebook
                    SET phone = %s, email = %s, birthday = %s, group_id = %s
                    WHERE id = %s;
                """, (main_phone, email, birthday, group_id, existing[0]))
                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (existing[0],))
                for ph in extra_phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (existing[0], ph["phone"], ph["type"]),
                    )
                overwritten += 1
                print(f"  '{username}' overwritten.")
            else:
                group_id = _resolve_group_id(cur, group_name)
                cur.execute("""
                    INSERT INTO phonebook (username, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (username, main_phone, email, birthday, group_id))
                new_id = cur.fetchone()[0]
                for ph in extra_phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (new_id, ph["phone"], ph["type"]),
                    )
                inserted += 1
                print(f"  '{username}' inserted.")

        conn.commit()
        print(f"\nImport done — inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}.")
    except Exception as e:
        conn.rollback()
        print("Error in import_from_json:", e)
    finally:
        cur.close()
        conn.close()


# ── CSV import ────────────────────────────────────────────────────────────────

def import_from_csv(filepath: str = "contacts.csv"): # <--- 1. ПЕРЕИМЕНОВАЛ
    """Extended CSV import with KZ phone validation."""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    inserted = skipped = errors = 0

    try:
        # <--- 2. ИСПРАВИЛ ЛОГИКУ НА CSV.DictReader
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                username   = row.get("username", "").strip()
                phone      = row.get("phone", "").strip()
                email      = row.get("email", "").strip() or None
                birthday   = row.get("birthday", "").strip() or None
                group_name = row.get("group", "").strip() or None
                phone_type = row.get("phone_type", "mobile").strip().lower()

                if not username or not phone:
                    print(f"  [SKIP] Missing username or phone: {row}")
                    skipped += 1
                    continue

                if not is_valid_kz_phone(phone):
                    print(f"  [SKIP] Invalid phone '{phone}' for '{username}'")
                    skipped += 1
                    continue
                phone = normalize_phone(phone)

                if phone_type not in ("home", "work", "mobile"):
                    phone_type = "mobile"

                try:
                    # Upsert основного контакта
                    cur.execute("CALL upsert_user(%s, %s);", (username, phone))
                    
                    # Получаем ID для дальнейших операций
                    cur.execute(
                        "SELECT id FROM phonebook WHERE username ILIKE %s LIMIT 1;",
                        (username,)
                    )
                    contact_id = cur.fetchone()[0]
                    
                    # Обновляем доп. поля
                    group_id = _resolve_group_id(cur, group_name)
                    cur.execute("""
                        UPDATE phonebook
                        SET email    = COALESCE(%s, email),
                            birthday = COALESCE(%s::DATE, birthday),
                            group_id = COALESCE(%s, group_id)
                        WHERE id = %s;
                    """, (email, birthday, group_id, contact_id))
                    
                    # Добавляем телефон в таблицу phones
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
                    """, (contact_id, phone, phone_type))
                    inserted += 1
                except Exception as row_err:
                    print(f"  [ERROR] Row {row}: {row_err}")
                    errors += 1

        conn.commit()
        print(f"\nCSV import done — processed: {inserted}, skipped: {skipped}, errors: {errors}.")
    except Exception as e:
        conn.rollback()
        print("Error in import_from_csv:", e)
    finally:
        cur.close()
        conn.close()

# ── JSON import ────────────────────────────────────────────────────────────────
def import_from_json(filepath: str = "contacts_export.json"):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
            return

    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    inserted = skipped = overwritten = 0

    try:
        for contact in data:
            username     = contact.get("username", "").strip()
            main_phone   = contact.get("main_phone", "")
            email        = contact.get("email")
            birthday     = contact.get("birthday")
            group_name   = contact.get("group")
            extra_phones = contact.get("extra_phones", [])

            if not username:
                print("  Skipping entry with no username.")
                skipped += 1
                continue

            if not is_valid_kz_phone(main_phone):
                print(f"  Skipping '{username}': invalid phone '{main_phone}'")
                skipped += 1
                continue
            main_phone = normalize_phone(main_phone)

            valid_extra = []
            for ph in extra_phones:
                num = ph.get("phone", "")
                if is_valid_kz_phone(num):
                    valid_extra.append({"phone": normalize_phone(num), "type": ph.get("type", "mobile")})
                else:
                    print(f"  Skipping invalid extra phone '{num}' for '{username}'")
            extra_phones = valid_extra

            # Check duplicate by username
            cur.execute(
                "SELECT id FROM phonebook WHERE username ILIKE %s LIMIT 1;",
                (username,)
            )
            existing_by_name = cur.fetchone()

            # Check duplicate by phone
            cur.execute(
                "SELECT id, username FROM phonebook WHERE phone = %s LIMIT 1;",
                (main_phone,)
            )
            existing_by_phone = cur.fetchone()

            # Phone belongs to a different user
            if existing_by_phone and (not existing_by_name or existing_by_phone[0] != existing_by_name[0]):
                print(f"\n  Phone '{main_phone}' already belongs to '{existing_by_phone[1]}'")
                print(f"  Cannot assign it to '{username}'")
                choice = input("  (s)kip, (r)eplace owner, or (n)ew phone? ").strip().lower()
                if choice == "r":
                    # Remove phone from old owner, assign to new
                    cur.execute("UPDATE phonebook SET phone = NULL WHERE id = %s;", (existing_by_phone[0],))
                    print(f"  Phone removed from '{existing_by_phone[1]}'")
                elif choice == "n":
                    main_phone_new = input_phone(f"  Enter new phone for '{username}': ")
                    if main_phone_new is None:
                        skipped += 1
                        continue
                    main_phone = main_phone_new
                else:
                    skipped += 1
                    continue

            if existing_by_name:
                print(f"\n  Duplicate found: '{username}'")
                choice = input("  (s)kip or (o)verwrite? ").strip().lower()
                if choice != "o":
                    skipped += 1
                    continue

                group_id = _resolve_group_id(cur, group_name)
                cur.execute("""
                    UPDATE phonebook
                    SET phone = %s, email = %s, birthday = %s, group_id = %s
                    WHERE id = %s;
                """, (main_phone, email, birthday, group_id, existing_by_name[0]))

                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (existing_by_name[0],))
                for ph in extra_phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (existing_by_name[0], ph["phone"], ph["type"]),
                    )
                overwritten += 1
                print(f"  '{username}' overwritten.")
            else:
                group_id = _resolve_group_id(cur, group_name)
                cur.execute("""
                    INSERT INTO phonebook (username, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (username, main_phone, email, birthday, group_id))
                new_id = cur.fetchone()[0]

                for ph in extra_phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (new_id, ph["phone"], ph["type"]),
                    )
                inserted += 1
                print(f"  '{username}' inserted.")

        conn.commit()
        print(f"\nImport done — inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}.")
    except Exception as e:
        conn.rollback()
        print("Error in import_from_json:", e)
    finally:
        cur.close()
        conn.close()


# ── New stored procedure wrappers ─────────────────────────────────────────────

def add_phone(contact_name: str, phone: str, phone_type: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (contact_name, phone, phone_type))
        conn.commit()
        print(f"  Phone {phone} ({phone_type}) added to '{contact_name}'.")
    except Exception as e:
        conn.rollback()
        print("Error in add_phone:", e)
    finally:
        cur.close()
        conn.close()


def move_to_group(contact_name: str, group_name: str):
    conn = connect()
    if conn is None:
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))
        conn.commit()
        print(f"  '{contact_name}' moved to group '{group_name}'.")
    except Exception as e:
        conn.rollback()
        print("Error in move_to_group:", e)
    finally:
        cur.close()
        conn.close()


# ── Menu ──────────────────────────────────────────────────────────────────────

def menu():
    init_schema()

    while True:
        print("""
╔══════════════════════════════════════════╗
║          PHONEBOOK — TSIS 1 MENU         ║
╠══════════════════════════════════════════╣
║  SEARCH & VIEW                           ║
║   1. Search contacts (name/phone/email)  ║
║   2. Filter by group                     ║
║   3. Search by email                     ║
║   4. Show all contacts (sorted)          ║
║   5. Browse contacts (page by page)      ║
╠══════════════════════════════════════════╣
║  CRUD                                    ║
║   6. Insert / update one user            ║
║   7. Insert many users                   ║
║   8. Delete by username                  ║
║   9. Delete by phone                     ║
╠══════════════════════════════════════════╣
║  PHONES & GROUPS                         ║
║  10. Add extra phone to contact          ║
║  11. Move contact to group               ║
╠══════════════════════════════════════════╣
║  IMPORT / EXPORT                         ║
║  12. Export contacts to JSON             ║
║  13. Import contacts from JSON           ║
║  14. Import contacts from CSV            ║
╠══════════════════════════════════════════╣
║   0. Exit                                ║
╚══════════════════════════════════════════╝""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            pattern = input("Search pattern: ").strip()
            search_contacts(pattern)

        elif choice == "2":
            group = input("Group name (Family/Work/Friend/Other): ").strip()
            sort  = _pick_sort()
            filter_by_group(group, sort)

        elif choice == "3":
            email = input("Email fragment (e.g. gmail): ").strip()
            sort  = _pick_sort()
            search_by_email(email, sort)

        elif choice == "4":
            sort = _pick_sort()
            show_all_sorted(sort)

        elif choice == "5":
            try:
                page_size = int(input("Page size [5]: ").strip() or "5")
            except ValueError:
                page_size = 5
            paginated_navigation(page_size)

        elif choice == "6":
            username = input("Username: ").strip()
            if not username:
                print("  Username cannot be empty.")
            else:
                phone = input_phone()
                if phone:
                    upsert_user(username, phone)

        elif choice == "7":
            try:
                n = int(input("How many users? "))
            except ValueError:
                print("  Invalid number.")
                input("\nPress Enter to continue...")
                continue

            usernames, phones, cancelled = [], [], False
            for i in range(n):
                print(f"\n  User #{i + 1}:")
                username = input("    Username: ").strip()
                if not username:
                    print("    Username cannot be empty. Cancelled.")
                    cancelled = True
                    break
                phone = input_phone("    Phone (+7XXXXXXXXXX): ")
                if phone is None:
                    cancelled = True
                    break
                usernames.append(username)
                phones.append(phone)

            if not cancelled:
                insert_many_users(usernames, phones)

        elif choice == "8":
            username = input("Username to delete: ").strip()
            delete_user_by_username(username)

        elif choice == "9":
            phone = input_phone("Phone to delete (+7XXXXXXXXXX): ")
            if phone:
                delete_user_by_phone(phone)

        elif choice == "10":
            name  = input("Contact name: ").strip()
            phone = input_phone()
            if phone:
                ptype = input("Type (home/work/mobile): ").strip().lower()
                if ptype not in ("home", "work", "mobile"):
                    print("  Invalid type. Use: home, work, mobile")
                else:
                    add_phone(name, phone, ptype)

        elif choice == "11":
            name  = input("Contact name: ").strip()
            group = input("Target group: ").strip()
            move_to_group(name, group)

        elif choice == "12":
            path = input("Output file [contacts_export.json]: ").strip() or "contacts_export.json"
            export_to_json(path)

        elif choice == "13":
            path = input("JSON file [contacts_export.json]: ").strip() or "contacts_export.json"
            import_from_json(path)

        elif choice == "14":
            path = input("CSV file [contacts.csv]: ").strip() or "contacts.csv"
            import_from_csv(path)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice. Try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()