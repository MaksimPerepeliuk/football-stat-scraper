from tqdm import tqdm
from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from multiprocessing import Pool
from functools import partial
from stat_scraper.utils import chunk
from stat_scraper.db_manager import select_all_urls
from stat_scraper.utils import time_track


def run_parse(filename, url):
    summary_stat = {}
    try:
        summary_stat.update(get_live_stat(url))
        summary_stat.update(get_past_stat(url))
    except Exception:
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')


@time_track
def run_multi_parse(urls, n_proc):
    app_logger.info(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    print(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    pool = Pool(n_proc)
    filename = f'tests/{n_proc}proc_result.txt'
    func = partial(run_parse, filename)
    pool.map(func, urls)
    pool.close()
    pool.join()
    return {
        'process_type': 'multiprocessing',
        'worker_amount': n_proc,
        'urls_count': len(urls)
    }


def main(n_proc=2):
    urls = select_all_urls()[:30]
    urls_chunks = chunk(urls, n_proc)
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, n_proc)


if __name__ == '__main__':
    for n_proc in range(10, 40, 4):
        main(n_proc)
