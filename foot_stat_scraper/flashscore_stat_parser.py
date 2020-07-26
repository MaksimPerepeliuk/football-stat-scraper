from events_urls_parser import driver  # в отдельный модуль
from bs4 import BeautifulSoup
import time


def get_goal_minutes(event_info_html):
    soup = BeautifulSoup(event_info_html, 'lxml')
    goal_icons = soup.select('div.icon-box.soccer-ball')
    goal_minutes = [goal_icon.findPreviousSibling().text.strip("'")
                    for goal_icon in goal_icons]
    return '-'.join(goal_minutes)


def normalize_feature(feature):
    return '_'.join(feature.lower().strip('%').split(' '))


def get_half_stats(url):
    driver.get(url)
    time.sleep(0.5)
    half_stat_html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(half_stat_html, 'lxml')
    stat_rows = soup.select('div.statRow')
    half_stats = {}
    for stat_row in stat_rows:
        title_value = normalize_feature(stat_row.select(
            'div.statText.statText--titleValue')[0].text)
        home_value = normalize_feature(stat_row.select(
            'div.statText.statText--homeValue')[0].text)
        away_value = normalize_feature(stat_row.select(
            'div.statText.statText--awayValue')[0].text)
        half_stats[f'{title_value}_home'] = int(home_value)
        half_stats[f'{title_value}_away'] = int(away_value)
    print(half_stats)


def get_summary_stat(url):
    driver.get(url)
    time.sleep(0.5)
    match_summary_html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(match_summary_html, 'lxml')
    championate_info = soup.select(
        'span.description__country')[0].text
    country = championate_info.split(':')[0]
    championate = championate_info.split(':')[1].split('-')[0]
    round_num = championate_info.split(':')[1].split('-')[1]
    date = soup.select('div#utime')[0].text.split(' ')[0]
    home_command = soup.select(
        'div.team-text.tname-home a.participant-imglink')[0].text
    away_command = soup.select(
        'div.team-text.tname-away a.participant-imglink')[0].text
    result_score = soup.select(
        'div#event_detail_current_result')[0].text.strip()
    detail_info = soup.select(
        'div.detailMS')[0]
    goal_minutes = get_goal_minutes(detail_info.encode_contents())
    first_half_url = url + '#match-statistics;1'
    second_half_url = url + '#match-statistics;2'
    get_half_stats(first_half_url)


get_summary_stat('https://www.flashscore.com/match/C2xXOviA')
