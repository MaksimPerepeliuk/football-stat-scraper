from stat_scraper.init_driver import get_driver
from stat_scraper.logs.loggers import app_logger
from bs4 import BeautifulSoup
import time


def get_page_source(url):
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(0.5)
        html = driver.page_source
        driver.quit()
        app_logger.info(f'Received html {url}\n')
    except Exception:
        app_logger.exception(f'Error receive html {url}\n')
    return html


def get_goal_minutes(event_info_html):
    soup = BeautifulSoup(event_info_html, 'lxml')
    goal_icons = soup.select('div.icon-box.soccer-ball')
    goal_minutes = [goal_icon.findPreviousSibling().text.strip("'")
                    for goal_icon in goal_icons]
    return '-'.join(goal_minutes)


def normalize_value(value):
    return '_'.join(value.lower().strip('%').split(' '))


def get_half_stat(url, half, command_id=None):
    html = get_page_source(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.info(f'Start parsing HALF {half} stat for {url}\n')
    half_table = ('div#tab-statistics-1-statistic'
                  if half == '1st_half' else
                  'div#tab-statistics-2-statistic')
    stat_rows = soup.select(f'{half_table} div.statRow')
    half_stats = {}
    for stat_row in stat_rows:
        if command_id is not None:
            title_value = normalize_value(stat_row.select(
                'div.statText.statText--titleValue')[0].text)
            home_value = normalize_value(stat_row.select(
                'div.statText.statText--homeValue')[0].text)
            away_value = normalize_value(stat_row.select(
                'div.statText.statText--awayValue')[0].text)
            half_stats[f'{half}_{title_value}_OWN'] = int(
                [home_value, away_value][command_id])
            half_stats[f'{half}_{title_value}_ENEMY'] = int(
                [home_value, away_value][command_id - 1])
        else:
            title_value = normalize_value(stat_row.select(
                'div.statText.statText--titleValue')[0].text)
            home_value = normalize_value(stat_row.select(
                'div.statText.statText--homeValue')[0].text)
            away_value = normalize_value(stat_row.select(
                'div.statText.statText--awayValue')[0].text)
            half_stats[f'{half}_{title_value}_home'] = int(home_value)
            half_stats[f'{half}_{title_value}_away'] = int(away_value)
    app_logger.debug(f'Received HALF stat:\n{half_stats}\n')
    return half_stats


def get_main_stat(url):
    html = get_page_source(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.info(f'Start parsing MAIN stat for {url}\n')
    main_stat = {}
    try:
        championate_info = soup.select(
            'span.description__country')[0].text
        main_stat['country'] = championate_info.split(':')[0]
        main_stat['championate'] = championate_info.split(
            ':')[1].split('-')[0].strip()
        main_stat['round_num'] = championate_info.split(
            ':')[1].split('-')[1].strip()
        main_stat['date'] = soup.select('div#utime')[0].text.split(' ')[0]
        main_stat['home_command'] = soup.select(
            'div.team-text.tname-home a.participant-imglink')[0].text
        main_stat['away_command'] = soup.select(
            'div.team-text.tname-away a.participant-imglink')[0].text
        main_stat['result_score'] = soup.select(
            'div#event_detail_current_result')[0].text.strip()
        detail_info = soup.select('div.detailMS')[0]
        main_stat['goal_minutes'] = get_goal_minutes(
            detail_info.encode_contents())
    except Exception:
        app_logger.exception(f'Error receiving main stat elements {url}')
    return main_stat


def get_live_stat(url):
    live_stat = {}
    live_stat.update(get_main_stat(url))
    first_half_url = url + '#match-statistics;1'
    second_half_url = url + '#match-statistics;2'
    live_stat.update(get_half_stat(first_half_url, '1st_half'))
    live_stat.update(get_half_stat(second_half_url, '2nd_half'))
    app_logger.debug(f'Formed data dict with live stat:\n {live_stat}\n')
    return live_stat
