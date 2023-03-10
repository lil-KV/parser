import psycopg2
from src.config import DBNAME, USER, PASSWORD, HOST


FLATS_TABLE = 'flats'


def create_flats_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS flats(
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price INTEGER,
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP WITH TIME ZONE
                )''')

            cur.execute('''
            ALTER TABLE flats ALTER COLUMN square TYPE CHARACTER VARYING(1000)
        ''')


def insert_flat(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO flats 
            (link, reference, price, title, description, date, number, square, city, street_house, district, year, rooms, photos) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO
            UPDATE SET
            link = EXCLUDED.link,
            reference = EXCLUDED.reference,
            price = EXCLUDED.price,
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            date = EXCLUDED.date,
            number = EXCLUDED.number, 
            square = EXCLUDED.square, 
            city = EXCLUDED.city,
            street_house = EXCLUDED.street_house,
            district = EXCLUDED.district,
            year = EXCLUDED.year,
            rooms = EXCLUDED.rooms,
            photos = EXCLUDED.photos
            ''',
                        (flat.link, flat.reference, flat.price, flat.title, flat.description, flat.date, flat.number,
                         flat.square, flat.city, flat.street_house, flat.district, flat.year, flat.rooms, flat.photos
                         )
                        )


def get_not_posted_flats():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT link, price, number, city FROM flats
            WHERE is_tg_posted = false
          
            ''')

            return cur.fetchall()


def update_not_posted_flats():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''UPDATE flats SET
            is_tg_posted = true
          
            '''
                        )
