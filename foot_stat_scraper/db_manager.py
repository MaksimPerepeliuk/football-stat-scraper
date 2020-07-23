import psycopg2
import os
from dotenv import load_dotenv
from contextlib import closing

load_dotenv()


def insert_into_events_urls(url):
    connection = psycopg2.connect(dbname='football_stat', user='max',
                                  password=os.environ['PSQL_MAX_PASS'],
                                  host='localhost')

    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO events_urls (url) VALUES (%s);''', (url, ))
            conn.commit()
