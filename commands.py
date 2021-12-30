import sqlite3


def create_db():
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Person( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            name TEXT, \
            phone_number TEXT, \
            amount_due REAL DEFAULT 0 \
        )")
        cur.execute("CREATE TABLE IF NOT EXISTS Service( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            name TEXT, \
            price REAL \
        )")
        cur.execute("CREATE TABLE IF NOT EXISTS Service_Person( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            service_id INTEGER, \
            person_id INTEGER, \
            FOREIGN KEY(service_id) REFERENCES Service(ID), \
            FOREIGN KEY(person_id) REFERENCES Person(ID) \
            UNIQUE(service_id, person_id) \
        )")
        conn.commit()


def charge():
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Service"
        )
        services = cur.fetchall()
        print("services:", services)
        for service in services:
            print(service[0])
            cur.execute(
                "SELECT * FROM Service_Person WHERE service_id = ?",
                (service[0],)
            )
            persons = cur.fetchall()
            price = round(service[2] / len(persons), 2)
            print("price:", price)
            print("persons:", persons)
            for person in persons:
                cur.execute(
                    "UPDATE Person SET amount_due = amount_due + ? WHERE ID = ?",
                    (price, person[2])
                )
        conn.commit()


def add_service(name, price):
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Service(name, price) VALUES(?, ?)",
            (name, price)
        )
        conn.commit()


def add_person(name, phone_number):
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Person(name, phone_number) VALUES(?, ?)",
            (name, phone_number)
        )
        conn.commit()


def add_person_service(person_id, service_id):
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Service_Person(person_id, service_id) VALUES(?, ?)",
            (person_id, service_id)
        )
        conn.commit()


def pay(person_id, amount):
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE Person SET amount_due = amount_due - ? WHERE ID = ?",
            (amount, person_id)
        )
        conn.commit()


def list_people():
    print("People:")
    print(f'{"ID":<3} {"Name":<15} {"Phone Number":<20} {"Amount Due":<13} {"Services":<10}')
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Person"
        )
        people = cur.fetchall()
        for person in people:
            cur.execute(
                "SELECT * FROM Service_Person WHERE person_id = ?", (
                    person[0],)
            )
            services = cur.fetchall()
            service_names = []
            for service in services:
                # print(service)
                cur.execute(
                    "SELECT name FROM Service WHERE ID = ?", (
                        service[1],)
                )
                service_name = cur.fetchone()
                # print(service_name)
                service_names.append(service_name[0])
            print(
                f'{person[0]:<3} {person[1]:<15} {person[2]:<20} {person[3]:<13} {[name for name in service_names]}')


def list_services():
    print("Services:")
    with sqlite3.connect("db.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Service"
        )
        services = cur.fetchall()
        print(f'{"ID":<5}{"Name":<10}{"Price":<8}')
        for service in services:
            print(f"{service[0]:<3} {service[1]:<10} {service[2]:<8}")
