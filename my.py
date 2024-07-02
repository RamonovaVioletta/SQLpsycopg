import psycopg2
conn = psycopg2.connect( user="postgres",
                         password="Sogma!1939",
                         database="netology")


def drop_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE phone,
                DROP TABLE client
            );
            """)
        conn.commit()


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(80) NOT NULL,
                last_name VARCHAR(80) NOT NULL,
                email VARCHAR(80) NOT NULL UNIQUE
        );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES client(id),
                number VARCHAR(20) NOT NULL UNIQUE);
        """)
        conn.commit()


def add_new_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name,last_name,email)
            VALUES(%s,%s,%s) RETURNING id,first_name,last_name,email;
        """, (first_name, last_name, email))


def add_phone_number(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id,number)
            VALUES(%s,%s);
            """, (client_id, phone))
        conn.commit()


def change_data(conn, client_id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client
            SET first_name = %s WHERE id = %s;
            """, (first_name, client_id))

        cur.execute("""
            UPDATE client
            SET last_name = %s WHERE id = %s;
            """, (last_name, client_id))

        cur.execute("""
            UPDATE client
            SET email = %s WHERE id = %s;
            """, (email, client_id))

        cur.execute("""
             UPDATE phone
             SET number = %s WHERE client_id = %s;
             """, (number, client_id))

        conn.commit()


def delete_phone_number(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE client_id = %s AND number = %s;
            """, (client_id, number))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM phone WHERE client_id = %s;
           """, (client_id,))

        cur.execute("""
           DELETE FROM client WHERE id = %s;
           """, (client_id,))

        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT client.id, client.first_name, client.last_name, client.email, phone.number FROM client
            LEFT JOIN phone ON client.id = phone.client_id
            WHERE client.first_name = %s AND client.last_name = %s AND client.email = %s AND phone.number = %s;
            """, (first_name, last_name, email, phone))


if __name__ == "__main__":
    with psycopg2.connect(database='netology', user='postgres', password='Sogma!1939') as conn:
        create_db(conn)
        drop_db(conn)
        add_new_client(conn, 'Violetta', 'Ramonova', 'va.ramonova@sogma.ru')
        add_phone_number(conn, 1, '928976161')
        change_data(conn, 1, "Violetta", "Ramonova", "v.ramonova@mail.ru", "9284976161")
        delete_phone_number(conn, 1, "9284976161")
        delete_client(conn, 1)
        find_client(conn, "Violetta")


