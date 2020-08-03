import time
from tqdm import tqdm
from stat_scraper.utils import get_csv_rows
from tests.past_stat_smoke_test import write_file
from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from multiprocessing import Pool
from functools import partial
from stat_scraper.utils import chunk, send_email
from stat_scraper.db_manager import select_all_urls
from stat_scraper.utils import time_track
# from multiprocessing.dummy import Pool as ThreadPool


def get_average_time(filename='stat_scraper/logs/time_tracks/time_track_url.csv'):
    rows = get_csv_rows(filename)
    run_seconds = []
    for row in rows[1:]:
        run_seconds.append(float(row[0].split(',')[-1]))
    return round(sum(run_seconds) / len(run_seconds), 3)


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


def main(n_proc=2, mail_every_sec=60):
    urls = select_all_urls()[:30]
    urls_chunks = chunk(urls, 5)
    urls_processed = 0
    started_at = time.time()
    hour_detect = time.time()
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, n_proc)
        urls_processed += 10
        current_time = time.time()
        if current_time - hour_detect > mail_every_sec:
            hour_detect = current_time
            common_time_work = round((current_time - started_at) / 60, 2)
            send_email(
                f'SERVER #  URL`s processed - {urls_processed}, time work {common_time_work} min\n'
                f'Average time process 10 url = {get_average_time()} n_proc = {n_proc}')
    send_email('SERVER #   Main function finish!!!')


if __name__ == '__main__':
    for n_proc in range(1, 6):
        main(n_proc)
