import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from logs.loggers import app_logger
from db_manager import insert_into_ng_odds
from tqdm import tqdm
from multiprocessing import Pool
from math import ceil


def get_html(url):
    user_agent = UserAgent().chrome
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        app_logger.debug(f'Received html page {url} code = {r.status_code}')
        return r.text
    else:
        app_logger.exception(f'Error getting html page {url} {r.status_code}')
    print(r.ok)


def get_data_from_table(trs, type_odds=None):
    result = []
    for tr in trs[2:]:
        try:
            tds = tr.select('td')
            min_match = tds[0].text
            score = tds[1].text
            home_odds = tds[2].text
            draw_or_value = tds[3].text
            away_odds = tds[4].text
            status = tds[6].text
            variable_name = 'draw_odds' if type_odds == '1x2' else 'value'
        except Exception:
            app_logger.exception('Error received html element')

        result.append({'min_match': min_match, 'score': score,
                       'home_odds': home_odds,
                       f'{variable_name}': draw_or_value,
                       'away_odds': away_odds, 'status': status})
    return result


def select_stat_in_HT(stats, type_odds):
    stats_in_HT = []
    for stat in stats:
        if stat['min_match'] == 'HT':
            keys = [type_odds + '_' + key + '_HT' for key in stat.keys()]
            new_stats = [{key: value}
                         for key, value in zip(keys, stat.values())]
            [stats_in_HT.append(new_stat) for new_stat in new_stats]
    return stats_in_HT


def select_pre_match_line(stats, type_odds):
    pre_match_line = []
    for stat in stats:
        if stat['status'].strip() == 'Live':
            pre_match_line.append(stat)
    if type_odds == '1x2':
        return {f'open_{type_odds}_home_odds': pre_match_line[-1]['home_odds'],
                f'close_{type_odds}_home_odds': pre_match_line[0]['home_odds'],
                f'open_{type_odds}_draw_odds': pre_match_line[-1]['draw_odds'],
                f'close_{type_odds}_draw_odds': pre_match_line[0]['draw_odds'],
                f'open_{type_odds}_away_odds': pre_match_line[-1]['away_odds'],
                f'close_{type_odds}_away_odds': pre_match_line[0]['away_odds']}
    return {f'open_{type_odds}_value': pre_match_line[-1]['value'],
            f'close_{type_odds}_value': pre_match_line[0]['value'],
            f'open_{type_odds}_home_odds': pre_match_line[-1]['home_odds'],
            f'close_{type_odds}_home_odds': pre_match_line[0]['home_odds'],
            f'open_{type_odds}_away_odds': pre_match_line[-1]['away_odds'],
            f'close_{type_odds}_away_odds': pre_match_line[0]['away_odds']}


def get_match_info(soup):
    a = soup.select('div.fbheader a')
    date_block = soup.select('div.fbheader div.row script')
    date_parts = str(date_block[0].contents[0]).split("'")[1].split(',')
    date = str(datetime.date(int(date_parts[0]),
                             int(date_parts[1]) + 1,
                             int(date_parts[2])))
    champ_name = a[0].text[1:-1]
    home_command = a[1].text
    away_command = a[2].text
    return {'date': date,
            'championate': champ_name,
            'home_command': home_command,
            'away_command': away_command}


def insert_stat(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        HDA_odds, AH_odds, OU_odds = soup.select('div#oddsDetai div')[0:3]
        HDA_stat = get_data_from_table(HDA_odds.select('tr'), '1x2')
        AH_stat = get_data_from_table(AH_odds.select('tr'))
        OU_stat = get_data_from_table(OU_odds.select('tr'))
        app_logger.debug('Received HDA, AH, OU statistics by minutes')
        summary_stats = {}
        summary_stats.update(select_pre_match_line(HDA_stat, '1x2'))
        summary_stats.update(select_pre_match_line(AH_stat, 'AH'))
        summary_stats.update(select_pre_match_line(OU_stat, 'OU'))
        app_logger.debug('Added prematch line move')
        [summary_stats.update(stat)
         for stat in select_stat_in_HT(HDA_stat, '1x2')]
        [summary_stats.update(stat)
         for stat in select_stat_in_HT(AH_stat, 'AH')]
        [summary_stats.update(stat)
         for stat in select_stat_in_HT(OU_stat, 'OU')]
        summary_stats.update(get_match_info(soup))
        app_logger.info(
            f'Formed objects with stats cnt keys={len(summary_stats.keys())}')
    except Exception:
        app_logger.exception('\nError received stats from elements page')
    insert_into_ng_odds(summary_stats)
    app_logger.debug('Record values in table\n')


def get_convert_urls():
    urls = open('foot_stat_scraper/urls/now_goal_urls.txt').read().split(', ')
    template = 'http://data.nowgoal.group/3in1odds/{}'
    new_urls = []
    for url in urls:
        tail_url = '3_' + url.split('/')[-1]
        new_urls.append(template.format(tail_url))
    unique_new_urls = list(set(new_urls))
    return unique_new_urls


def main(urls):
    for url in tqdm(urls):
        try:
            insert_stat(get_html(url))
        except Exception:
            app_logger.debug('\nError records values in database')


def partial(data, parts_count):
    part_len = ceil((len(data) / parts_count))
    result = []
    for i in range(0, len(data), part_len):
        result.append(data[i:i+part_len])
    return result


def start_parallel_exec(f, args, count):
    partial_args = partial(args, count)
    with Pool(count) as p:
        p.map(f, partial_args)


if __name__ == '__main__':
    urls = get_convert_urls()
    start_parallel_exec(main, urls, 10)
