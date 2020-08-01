from math import ceil
from csv import DictWriter
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


def chunk(data, n_chunc):
    part_len = ceil((len(data) / n_chunc))
    result = []
    for i in range(0, len(data), part_len):
        result.append(data[i:i+part_len])
    return result


def write_csv(filename, data, order):
    with open(filename, 'a') as file:
        writer = DictWriter(file, fieldnames=order)
        is_empty = os.stat(filename).st_size == 0
        if is_empty:
            writer.writeheader()
        writer.writerow(data)
