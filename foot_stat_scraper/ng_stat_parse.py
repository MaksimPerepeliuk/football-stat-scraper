import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from logs.loggers import app_logger


def convert_urls():
    urls = open('foot_stat_scraper/urls/now_goal_urls.txt').read().split(', ')
    template = 'http://data.nowgoal.group/3in1odds/{}'
    new_urls = []
    for url in urls:
        tail_url = '3_' + url.split('/')[-1]
        new_urls.append(template.format(tail_url))
    unique_new_urls = list(set(new_urls))
    return unique_new_urls


def get_html(url):
    user_agent = UserAgent().chrome
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.ok:
        return r.text
        app_logger.debug(f'Received html page {r.status_code}')
    else:
        app_logger.exception(f'Error getting html page {r.status_code}')
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


def replace_HT(stats):
    for stat in stats:
        stat['min_match'] = stat['min_match'].replace('HT', '450')
    return stats


def select_stat_by_minutes(stats, interval_minutes=10):
    stats_only_run = replace_HT(
        list(filter(lambda stat: stat['status'] == 'Run', stats)))
    run_minute = int(stats_only_run[-1]['min_match'])
    stats_by_interval = []
    for stat in stats_only_run[::-1]:
        minute = int(stat['min_match'])
        if minute >= run_minute + interval_minutes:
            stats_by_interval.append(stat)
            run_minute = minute if minute != 450 else 45
    return stats_by_interval


def select_pre_match_line(stats, type_odds):
    pre_match_line = []
    for stat in stats:
        if stat['status'] == 'Live':
            pre_match_line.append(stat)
    if type_odds == '1x2':
        return {f'open_{type_odds}_home_odds': pre_match_line[-1]['home_odds'],
                f'close_{type_odds}_home_odds': pre_match_line[0]['home_odds'],
                f'open_{type_odds}_draw_odds': pre_match_line[-1]['draw_odds'],
                f'close_{type_odds}_draw_odds': pre_match_line[0]['draw_odds'],
                f'open_{type_odds}_away_odds': pre_match_line[-1]['away_odds'],
                f'close_{type_odds}_away_odds': pre_match_line[0]['away_odds']}

    return {f'open_{type_odds}_home_odds': pre_match_line[-1]['home_odds'],
            f'close_{type_odds}_home_odds': pre_match_line[0]['home_odds'],
            f'open_{type_odds}_away_odds': pre_match_line[-1]['away_odds'],
            f'close_{type_odds}_away_odds': pre_match_line[0]['away_odds']}


def get_stat(html):
    soup = BeautifulSoup(html, 'lxml')
    HDA_odds, AH_odds, OU_odds = soup.select('div#oddsDetai div')[0:3]
    HDA_stat = get_data_from_table(HDA_odds.select('tr'), '1x2')
    AH_stat = get_data_from_table(AH_odds.select('tr'))
    OU_stat = get_data_from_table(OU_odds.select('tr'))
    open_close_HDA = select_pre_match_line(HDA_stat, '1x2')
    open_close_AH = select_pre_match_line(HDA_stat, 'AH')
    open_close_OU = select_pre_match_line(HDA_stat, 'OU')
    print(111111111, select_stat_by_minutes(OU_stat))


get_stat(get_html('http://data.nowgoal.group/3in1odds/3_861230.html'))
