from stat_scraper.utils import time_track, write_csv, send_email
from stat_scraper.utils import chunk, write_text_file
from stat_scraper.fs_live_stat_parser import get_live_stat
from stat_scraper.fs_past_stat_parser import get_past_stat
from stat_scraper.logs.loggers import app_logger
from multiprocessing import Pool
from functools import partial
from tqdm import tqdm


SERVER_NAME = 'server#1'


def normalize_data(data):
    new_keys_file = open('stat_scraper/scripts/keys/new_keys.txt')
    old_keys_file = open('stat_scraper/scripts/keys/old_keys.txt')
    new_keys = new_keys_file.read().split('\n')
    old_keys = old_keys_file.read().split('\n')
    new_keys_file.close()
    old_keys_file.close()
    normalized_dict = {}
    for new_key, old_key in zip(new_keys, old_keys):
        normalized_dict[new_key] = data.get(old_key, None)
    return normalized_dict


def run_parse(filename, url):
    summary_stat = {}
    try:
        summary_stat.update(get_live_stat(url))
        summary_stat.update(get_past_stat(url))
    except Exception:
        write_text_file('stat_scraper/urls/failed_urls.txt', url)
        app_logger.exception(f'ERROR RUN PARSE ON URL {url}')
    data = normalize_data(summary_stat)
    write_csv(filename, data, data.keys())


@time_track
def run_multi_parse(urls, n_proc):
    app_logger.info(f'Start multiprocess function urls - {len(urls)} num processes - {n_proc}')
    pool = Pool(n_proc)
    filename = f'stat_scraper/scripts/fs_foot_stat_{SERVER_NAME}.csv'
    func = partial(run_parse, filename)
    pool.map(func, urls)
    pool.close()
    pool.join()
    return {
        'process_type': 'multiprocessing',
        'worker_amount': n_proc,
        'urls_count': len(urls)
    }


def main(n_proc):
    urls = open('stat_scraper/urls/events_urls.txt').read().split(', ')[:30]
    urls_chunks = chunk(urls, 10)
    for urls_chunk in tqdm(urls_chunks):
        run_multi_parse(urls_chunk, n_proc)


if __name__ == '__main__':
    main(10)
    send_email(f'{SERVER_NAME}: Main function finish!!!')
