from tests.past_stat_smoke_test import urls, run
import time
import csv
import os


def write_csv(filename, data, order):
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=order)
        is_empty = os.stat(filename).st_size == 0
        if is_empty:
            writer.writeheader()
        writer.writerow(data)


def time_track(func):
    def surrogate(*args):
        started_at = time.time()

        result = func(*args)

        ended_at = time.time()
        data = {}
        data.update(result)
        data['running_time'] = round(ended_at - started_at, 4)
        write_csv('time_track.csv', data,
                  ['process_type', 'worker_amount',
                   'running_time', 'urls_count'])
    return surrogate


@time_track
def func(n):
    a = 10000 ** 1000000 + n
    return {
        'process_type': 'multithreading',
        'worker_amount': 1,
        'urls_count': n
    }


func(10)
