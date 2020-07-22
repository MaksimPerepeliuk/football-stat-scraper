import psycopg2
import os
from dotenv import load_dotenv
from contextlib import closing

load_dotenv()


def insert_into_champ_urls(country, season, championate, url):
    connection = psycopg2.connect(dbname='football_stat', user='max',
                                  password=os.environ['PSQL_MAX_PASS'],
                                  host='localhost')

    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO champ_urls (country, season, championate, url)
                           VALUES (%s, %s, %s, %s);''',
                           (country, season, championate, url))
            conn.commit()
