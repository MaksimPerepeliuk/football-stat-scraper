import csv
import time
import os
import smtplib
from dotenv import load_dotenv


def send_email(msg):
    load_dotenv()
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(os.environ['EMAIL1'], os.environ['EMAIL_PASS'])
    smtpObj.sendmail(
        os.environ['EMAIL1'], os.environ['EMAIL2'], f'{msg}')
    smtpObj.quit()


def chunk(list_, size):
    result = []
    chunk = []
    for elem in list_:
        if len(chunk) == size:
            result.append(chunk)
            chunk = []
        chunk.append(elem)
    result.append(chunk)
    return result


def write_csv(filename, data, order):
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=order)
        is_empty = os.stat(filename).st_size == 0
        if is_empty:
            writer.writeheader()
        writer.writerow(data)


def time_track(func):

    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args)

        ended_at = time.time()

        result['running_time'] = round(ended_at - started_at, 4)
        write_csv('stat_scraper/logs/time_tracks/time_track_url.csv', result,
                  ['process_type', 'worker_amount',
                   'urls_count', 'running_time'])
    return surrogate


def get_csv_rows(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            rows.append(row)
    return rows


def write_text_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}, ')
