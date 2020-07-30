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
                """INSERT INTO events_urls (url) VALUES (%s);""", (url, ))
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


def insert_into_ng_odds(stat):
    connection = psycopg2.connect(dbname='football_stat', user='max',
                                  password=os.environ['PSQL_MAX_PASS'],
                                  host='localhost')
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""INSERT INTO ng_odds_stat (date, championate, home_command,
                           away_command, open_1x2_home, close_1x2_home,
                           open_1x2_draw, close_1x2_draw, open_1x2_away,
                           close_1x2_away, open_AH_value, close_AH_value,
                           open_AH_home, close_AH_home,
                           open_AH_away, close_AH_away, open_OU_value,
                           close_OU_value, open_OU_over,
                           close_OU_over, open_OU_under, close_OU_under,
                           HT_score, HT_AH_value, HT_AH_home, HT_AH_away,
                           HT_OU_value, HT_OU_over, HT_OU_under)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                           (stat.get('date', None),
                            stat.get('championate', None),
                            stat.get('home_command', None),
                            stat.get('away_command', None),
                            stat.get('open_1x2_home_odds', None),
                            stat.get('close_1x2_home_odds', None),
                            stat.get('open_1x2_draw_odds', None),
                            stat.get('close_1x2_draw_odds', None),
                            stat.get('open_1x2_away_odds', None),
                            stat.get('close_1x2_away_odds', None),
                            stat.get('open_AH_value', None),
                            stat.get('close_AH_value', None),
                            stat.get('open_AH_home_odds', None),
                            stat.get('close_AH_home_odds', None),
                            stat.get('open_AH_away_odds', None),
                            stat.get('close_AH_away_odds', None),
                            stat.get('open_OU_value', None),
                            stat.get('close_OU_value', None),
                            stat.get('open_OU_home_odds', None),
                            stat.get('close_OU_home_odds', None),
                            stat.get('open_OU_away_odds', None),
                            stat.get('close_OU_away_odds', None),
                            stat.get('AH_score_HT', None),
                            stat.get('AH_value_HT', None),
                            stat.get('AH_home_odds_HT', None),
                            stat.get('AH_away_odds_HT', None),
                            stat.get('OU_value_HT', None),
                            stat.get('OU_home_odds_HT', None),
                            stat.get('OU_away_odds_HT', None),))
            conn.commit()


def select_all_urls():
    connection = psycopg2.connect(dbname='football_stat', user='max',
                                  password=os.environ['PSQL_MAX_PASS'],
                                  host='localhost')
    with closing(connection) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT url FROM events_urls;')
            result = [url[0] for url in cursor.fetchall()]
            conn.commit()
            return result


# def insert_into_fs_foot_stat(stat):
#     connection = psycopg2.connect(dbname='football_stat', user='max',
#                                   password=os.environ['PSQL_MAX_PASS'],
#                                   host='localhost')
#     with closing(connection) as conn:
#         with conn.cursor() as cursor:
#             cursor.execute("""INSERT INTO ng_odds_stat (date, championate, home_command,
#                            away_command, open_1x2_home, close_1x2_home,
#                            open_1x2_draw, close_1x2_draw, open_1x2_away,
#                            close_1x2_away, open_AH_value, close_AH_value,
#                            open_AH_home, close_AH_home,
#                            open_AH_away, close_AH_away, open_OU_value,
#                            close_OU_value, open_OU_over,
#                            close_OU_over, open_OU_under, close_OU_under,
#                            HT_score, HT_AH_value, HT_AH_home, HT_AH_away,
#                            HT_OU_value, HT_OU_over, HT_OU_under)
#                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
#                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
#                            (stat.get('date', None),
#                             stat.get('championate', None),
#                             stat.get('home_command', None),
#                             stat.get('away_command', None),
#                             stat.get('open_1x2_home_odds', None),
#                             stat.get('close_1x2_home_odds', None),
#                             stat.get('open_1x2_draw_odds', None),
#                             stat.get('close_1x2_draw_odds', None),
#                             stat.get('open_1x2_away_odds', None),
#                             stat.get('close_1x2_away_odds', None),
#                             stat.get('open_AH_value', None),
#                             stat.get('close_AH_value', None),
#                             stat.get('open_AH_home_odds', None),
#                             stat.get('close_AH_home_odds', None),
#                             stat.get('open_AH_away_odds', None),
#                             stat.get('close_AH_away_odds', None),
#                             stat.get('open_OU_value', None),
#                             stat.get('close_OU_value', None),
#                             stat.get('open_OU_home_odds', None),
#                             stat.get('close_OU_home_odds', None),
#                             stat.get('open_OU_away_odds', None),
#                             stat.get('close_OU_away_odds', None),
#                             stat.get('AH_score_HT', None),
#                             stat.get('AH_value_HT', None),
#                             stat.get('AH_home_odds_HT', None),
#                             stat.get('AH_away_odds_HT', None),
#                             stat.get('OU_value_HT', None),
#                             stat.get('OU_home_odds_HT', None),
#                             stat.get('OU_away_odds_HT', None),))
#             conn.commit()
