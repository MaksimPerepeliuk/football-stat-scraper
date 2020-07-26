from init_driver import get_driver
from bs4 import BeautifulSoup
from logs.loggers import app_logger
import time


def get_html(url):
    try:
        driver = get_driver()
        driver.get(url)
        time.sleep(0.2)
        html = driver.page_source
        driver.quit()
        app_logger.debug(f'Received html {url}')
    except Exception:
        app_logger.exception(f'Error receive html {url}')
    return html


def get_goal_minutes(event_info_html):
    soup = BeautifulSoup(event_info_html, 'lxml')
    goal_icons = soup.select('div.icon-box.soccer-ball')
    goal_minutes = [goal_icon.findPreviousSibling().text.strip("'")
                    for goal_icon in goal_icons]
    return '-'.join(goal_minutes)


def normalize_value(value):
    return '_'.join(value.lower().strip('%').split(' '))


def get_half_stat(url, half):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    stat_rows = soup.select('div.statRow')
    half_stats = {}
    for stat_row in stat_rows:
        try:
            title_value = normalize_value(stat_row.select(
                'div.statText.statText--titleValue')[0].text)
            home_value = normalize_value(stat_row.select(
                'div.statText.statText--homeValue')[0].text)
            away_value = normalize_value(stat_row.select(
                'div.statText.statText--awayValue')[0].text)
            half_stats[f'{half}_{title_value}_home'] = int(home_value)
            half_stats[f'{half}_{title_value}_away'] = int(away_value)
        except Exception:
            app_logger.exception(f'\n Error receive half stat in {url}')
    return half_stats


def get_main_stat(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.debug(f'Start collect main stat data from {url}')
    main_stat = {}
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
    main_stat['goal_minutes'] = get_goal_minutes(detail_info.encode_contents())
    return main_stat


def insert_live_stat(url):
    try:
        live_stat = {}
        live_stat.update(get_main_stat(url))
        first_half_url = url + '#match-statistics;1'
        second_half_url = url + '#match-statistics;2'
        live_stat.update(get_half_stat(first_half_url, '1st_half'))
        live_stat.update(get_half_stat(second_half_url, '2nd_half'))
        app_logger.debug(f'Formed data dict with live stat:\n {live_stat}')
    except Exception:
        app_logger.exception(f'Error receive elements on {url}')
    print(live_stat)


def main():
    insert_live_stat('https://www.flashscore.com/match/C2xXOviA')


if __name__ == '__main__':
    main()
