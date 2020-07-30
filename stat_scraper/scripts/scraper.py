from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from stat_scraper.db_manager import select_all_urls
from stat_scraper.utils import partial
from multiprocessing import Pool
from tqdm import tqdm


def run_parse(n_worker, filename, url):
    try:
        summary_stat = {}
        summary_stat.update(get_live_stat(url))
        summary_stat.update(get_past_stat(url))
    except Exception:
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')


def run_multi_parse(urls, n_threads, type):
    pool = Pool(n_threads)
    filename = f'./tests/{n_threads}thread_result.txt'
    func = partial(run_parse, n_threads, filename)
    pool.map(func, urls)
    pool.close()
    pool.join()


if __name__ == '__main__':
    urls = select_all_urls()[:300]
    urls_partial = partial(urls)
    for urls_part in tqdm(urls_partial):
        run_multi_parse(urls_part, 10, 'multiprocessing [100:33]')
