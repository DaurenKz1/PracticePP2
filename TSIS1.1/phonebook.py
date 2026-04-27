import psycopg2
from config import load_config
import csv
import json


def search_contacts(query):
    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()

            for row in rows:
                print(row)


def read_all_contacts():
    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.first_name, c.last_name, c.email, c.birthday,
                       g.name AS group_name,
                       p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id
                ORDER BY c.id
            """)

            rows = cur.fetchall()

            for row in rows:
                print(row)


def insert_contact(first_name, last_name, email, birthday, group_name, phone, phone_type):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                # get or create group
                cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                group = cur.fetchone()

                if group is None:
                    cur.execute(
                        "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                        (group_name,))
                    group_id = cur.fetchone()[0]
                else:
                    group_id = group[0]

                # insert contact
                cur.execute("""
                    INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                    VALUES(%s,%s,%s,%s,%s)
                    RETURNING id
                """, (first_name, last_name, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                # insert phone
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s,%s,%s)
                """, (contact_id, phone, phone_type))

            conn.commit()

    except Exception as e:
        print(e)


def update_contact(contact_id):
    config = load_config()

    first_name = input("new first name: ")
    last_name = input("new last name: ")
    email = input("new email: ")
    birthday = input("new birthday (YYYY-MM-DD): ")

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:

            # update contact
            cur.execute("""
                UPDATE contacts
                SET first_name=%s,
                    last_name=%s,
                    email=%s,
                    birthday=%s
                WHERE id=%s
            """, (first_name, last_name, email, birthday, contact_id))

            # update phone (optional)
            change = input("Update phone? (yes/no): ")

            if change == "yes":
                phone = input("new phone: ")
                phone_type = input("type (home/work/mobile): ")

                cur.execute("""
                    UPDATE phones
                    SET phone=%s, type=%s
                    WHERE contact_id=%s
                """, (phone, phone_type, contact_id))

        conn.commit()

    print("Updated!")


def insert_from_csv():
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                with open("contacts.csv", "r") as file:
                    reader = csv.DictReader(file)

                    for row in reader:

                        # check if contact exists
                        cur.execute("""
                            SELECT id FROM contacts
                            WHERE first_name=%s AND last_name=%s
                        """, (row["first_name"], row["last_name"]))

                        result = cur.fetchone()

                        if result:
                            contact_id = result[0]
                        else:
                            # create group
                            cur.execute("SELECT id FROM groups WHERE name=%s", (row["group"],))
                            g = cur.fetchone()

                            if not g:
                                cur.execute(
                                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                                    (row["group"],))
                                group_id = cur.fetchone()[0]
                            else:
                                group_id = g[0]

                            # insert contact
                            cur.execute("""
                                INSERT INTO contacts(first_name,last_name,email,birthday,group_id)
                                VALUES(%s,%s,%s,%s,%s)
                                RETURNING id
                            """, (
                                row["first_name"],
                                row["last_name"],
                                row["email"],
                                row["birthday"],
                                group_id
                            ))

                            contact_id = cur.fetchone()[0]

                        # always insert phone
                        cur.execute("""
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES(%s,%s,%s)
                        """, (
                            contact_id,
                            row["phone"],
                            row["phone_type"]
                        ))

            conn.commit()

        print("CSV imported correctly!")

    except Exception as e:
        print(e)


def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def paginate():
    offset = 0
    limit = 3
    config = load_config()

    while True:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT first_name, last_name
                    FROM contacts
                    LIMIT %s OFFSET %s
                """, (limit, offset))

                rows = cur.fetchall()

                for r in rows:
                    print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break


def delete_contact():
    config = load_config()

    choice = input("Delete by (id/name): ")

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:

            if choice == "id":
                cid = input("Enter id: ")
                cur.execute("DELETE FROM contacts WHERE id=%s", (cid,))

            elif choice == "name":
                name = input("Enter first name: ")
                cur.execute("DELETE FROM contacts WHERE first_name=%s", (name,))

        conn.commit()

    print("Deleted!")


def export_json():
    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.first_name, c.last_name, c.email, c.birthday,
                       g.name, p.phone, p.type
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id
            """)

            data = cur.fetchall()

            result = []
            for row in data:
                result.append({
                    "first_name": row[0],
                    "last_name": row[1],
                    "email": row[2],
                    "birthday": str(row[3]),
                    "group": row[4],
                    "phone": row[5],
                    "type": row[6]
                })

            with open("contacts.json", "w") as f:
                json.dump(result, f, indent=4)

    print("Exported to JSON!")


def import_json():
    with open("contacts.json", "r") as f:
        data = json.load(f)

    for c in data:
        choice = input(f"{c['first_name']} exists? (skip/overwrite): ")

        if choice == "skip":
            continue

        insert_contact(
            c["first_name"],
            c["last_name"],
            c["email"],
            c["birthday"],
            c["group"],
            c["phone"],
            c["type"]
        )


def get_sorted(sort_by="first_name"):
    config = load_config()

    allowed = ["first_name", "birthday", "created_at"]
    if sort_by not in allowed:
        print("Invalid sort")
        return

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT first_name, last_name, email, birthday
                FROM contacts
                ORDER BY {sort_by}
            """)

            for row in cur.fetchall():
                print(row)


def filter_by_group(group_name):
    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.first_name, c.last_name, g.name, p.phone
                FROM contacts c
                JOIN groups g ON g.id = c.group_id
                LEFT JOIN phones p ON p.contact_id = c.id
                WHERE g.name = %s
            """, (group_name,))

            for row in cur.fetchall():
                print(row)


if __name__ == "__main__":
    print("Commands: add, csv, import, read, search, group, sort, pages, update, delete, export, exit")

    while True:
        cmd = input(">> ").lower().strip()

        if cmd == "add":
            insert_contact(
                input("first: "),
                input("last: "),
                input("email: "),
                input("birthday (YYYY-MM-DD): "),
                input("group: "),
                input("phone: "),
                input("type (home/work/mobile): ")
            )
        elif cmd == "csv":
            insert_from_csv()
        elif cmd == "search":
            search_contacts(input("query: "))
        elif cmd == "group":
            filter_by_group(input("group: "))
        elif cmd == "sort":
            get_sorted(input("sort by (first_name/birthday/created_at): "))
        elif cmd == "export":
            export_json()
        elif cmd == "read":
            read_all_contacts()
        elif cmd == "update":
            update_contact(int(input("contact id: ")))
        elif cmd == "delete":
            delete_contact()
        elif cmd == "import":
            import_json()
        elif cmd == "pages":
            paginate()
        elif cmd == "exit":
            break
        else:
            print("Unknown command. Available: add, csv, import, read, search, group, sort, pages, update, delete, export, exit")