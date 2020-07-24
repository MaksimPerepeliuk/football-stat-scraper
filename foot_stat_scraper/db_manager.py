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

# CREATE TABLE ng_odds_stat (
# 	id             bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
# 	date           varchar(255),
# 	championate    varchar(255),
# 	home_command   varchar(255),
# 	away_command   varchar(255),
# 	open_1x2_home  decimal,
# 	close_1x2_home decimal,
# 	open_1x2_draw  decimal,
# 	close_1x2_draw decimal,
# 	open_1x2_away  decimal,
# 	close_1x2_away decimal,
# 	open_AH_home   decimal,
# 	close_AH_home  decimal,
# 	open_AH_away   decimal,
# 	close_AH_away  decimal,
# 	open_OU_over   decimal,
# 	close_OU_under decimal,
# 	open_OU_over   decimal,
# 	close_OU_under decimal,
# 	HT_score       varchar(255),
# 	HT_AH_value	   varchar(255),
# 	HT_AH_home     decimal,
# 	HT_AH_away     decimal,
# 	HT_OU_value	   varchar(255),
# 	HT_OU_over     decimal,
# 	HT_OU_under    decimal,
# );


# def insert_into_ng_odds(obj):
#     connection = psycopg2.connect(dbname='football_stat', user='max',
#                                   password=os.environ['PSQL_MAX_PASS'],
#                                   host='localhost')

#     with closing(connection) as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(
#                 '''INSERT INTO ng_odds_stat (url) VALUES (%s);''', (url, ))
#             conn.commit()
