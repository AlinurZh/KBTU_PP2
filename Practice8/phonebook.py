from connect import connect

def search_contacts(pattern):
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        rows = cur.fetchall()
        print("\nSearch results:")
        if rows:
            for row in rows:
                print(row)
        else:
            print("No matching records found.")
    except Exception as e:
        print("Error in search_contacts", e)
    finally:
        cur.close()
        conn.close()

def upsert_user(username, phone):
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_user(%s, %s);", (username, phone))
        conn.commit()
        print(f"\nUser '{username}' inserted/updated successfully!")
    except Exception as e:
        conn.rollback()
        print("Error in upsert_user", e)
    finally:
        conn.close()
        cur.close()
    
def insert_many_users(usernames, phones):
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
        conn.commit()
        print("\nBulk insert completed!")
    except Exception as e:
        conn.rollback()
        print("Error in insert_many_users", e)
    finally:
        conn.close()
        cur.close()

def get_contacts_paginated(limit, offset):
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s), (limit, offset)")
        rows = cur.fetchall()
        print(f"\nPaginated results (LIMIT={limit}, OFFSET={offset}):")
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
    except Exception as e:
        print("Error in get_contacts_paginated", e)
    finally:
        conn.close()
        cur.close()

def delete_user_by_username(username):
    conn = connect()
    if conn is None:
        return 
    
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_user(%s, %s);", (username, None))
        conn.commit()
        print(f"\nUser with username '{username}' deleted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error in delete_user_by_username", e)
    finally:
        cur.close()
        conn.close()
        
def delete_user_by_phone(phone):
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_user(%s, %s);", (None, phone))
        conn.commit()
        print(f"\nUser with phone '{phone}' deleted successfully!")
    except Exception as e:
        print("Error in delete_user_by_phone:", e)
    finally:
        cur.close()
        conn.close()

def show_all_contacts():
    conn = connect()
    if conn is None:
        return
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM phonebook ORDER BY id;")
        rows = cur.fetchall()

        print("\nAll contacts:")
        if rows:
            for row in rows:
                print(row)
        else:
            print("Phonebook is empty")
    except Exception as e:
        print("Error in show_all_contacts:", e)
    finally:
        cur.close()
        conn.close()
def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Search contacts by pattern")
        print("2. Insert or update one user")
        print("3. Insert many users")
        print("4. Show contacts with pagination")
        print("5. Delete user by username")
        print("6. Delete user by phone")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pattern = input("Enter search pattern: ")
            search_contacts(pattern)

        elif choice == "2":
            username = input("Enter username: ")
            phone = input("Enter phone: ")
            upsert_user(username, phone)

        elif choice == "3":
            try:
                n = int(input("How many users do you want to insert? "))
                usernames = []
                phones = []

                for i in range(n):
                    username = input(f"Enter username #{i + 1}: ")
                    phone = input(f"Enter phone #{i + 1}: ")
                    usernames.append(username)
                    phones.append(phone)

                insert_many_users(usernames, phones)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            try:
                limit = int(input("Enter LIMIT: "))
                offset = int(input("Enter OFFSET: "))
                get_contacts_paginated(limit, offset)
            except ValueError:
                print("LIMIT and OFFSET must be integers.")

        elif choice == "5":
            username = input("Enter username to delete: ")
            delete_user_by_username(username)

        elif choice == "6":
            phone = input("Enter phone to delete: ")
            delete_user_by_phone(phone)

        elif choice == "7":
            show_all_contacts()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()


            


        