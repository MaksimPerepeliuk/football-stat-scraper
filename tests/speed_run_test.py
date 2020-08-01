import os
import csv
import time
from tqdm import tqdm
from tests.past_stat_smoke_test import write_file
from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from stat_scraper.utils import chunk, send_email
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
        write_csv('./tests/time_track_url.csv', result,
                  ['process_type', 'worker_amount',
                   'urls_count', 'running_time'])
    return surrogate


def run_parse(filename, url):
    summary_stat = {}
    try:
        summary_stat.update(get_live_stat(url))
        summary_stat.update(get_past_stat(url))
    except Exception:
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')
    write_file(filename, summary_stat)


@time_track
def run_multi_parse(urls, n_proc):
    app_logger.info(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    print(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    pool = Pool(n_proc)
    filename = f'./tests/{n_proc}proc_result.txt'
    func = partial(run_parse, filename)
    pool.map(func, urls)
    pool.close()
    pool.join()
    return {
        'process_type': 'multiprocessing',
        'worker_amount': n_proc,
        'urls_count': len(urls)
    }


if __name__ == '__main__':
    urls = select_all_urls()[:50]
    urls_chunks = chunk(urls, 10)
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, 10)
    send_email('speed run test finish!!!')
