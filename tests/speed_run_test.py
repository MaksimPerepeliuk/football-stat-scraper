import os
import csv
import time
from tqdm import tqdm
from tests.past_stat_smoke_test import urls, write_file
from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from stat_scraper.db_manager import select_all_urls


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
        write_csv('./tests/time_track.csv', result,
                  ['process_type', 'worker_amount',
                   'urls_count', 'running_time'])
    return surrogate


def run_parse(n_worker, filename, url):
    try:
        summary_stat = {}
        summary_stat.update(get_live_stat(url))
        summary_stat.update(get_past_stat(url))
        write_file(filename, summary_stat)
    except Exception:
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')


@time_track
def run_multi_parse(urls, n_threads, perf_type):
    pool = ThreadPool(n_threads)
    filename = f'./tests/{n_threads}thread_result.txt'
    func = partial(run_parse, n_threads, filename)
    pool.map(func, urls)
    pool.close()
    pool.join()
    return {
        'process_type': perf_type,
        'worker_amount': n_threads,
        'urls_count': len(urls)
    }


if __name__ == '__main__':
    # urls_partial = [urls[:3], urls[3:6], urls[6:9]]
    # for urls_part in tqdm(urls_partial):
    urls = select_all_urls()[:100] # 36 errors
    run_multi_parse(urls, 30, 'multithreading')
