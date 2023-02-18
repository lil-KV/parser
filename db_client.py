# одинаковый для всех ссылок
import psycopg2

DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = 'lk1118740'
HOST = '127.0.0.1'

FLATS_TABLE = 'flats'


def create_flats_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS flats(
                id serial,
                link CHARACTER VARYING(300),
                reference CHARACTER VARYING(30),
                price INTEGER,
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP WITH TIME ZONE)''')


def insert_flat(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO flats (link, reference, price, title, description, date) 
            VALUES (%s, %s, %s, %s, %s, %s)''',
                        (flat.link, flat.reference, flat.price, flat.title, flat.description, flat.date)
                        )

