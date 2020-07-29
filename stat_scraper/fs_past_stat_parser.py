from stat_scraper.fs_live_stat_parser import get_html, get_main_stat
from stat_scraper.fs_live_stat_parser import get_half_stat
from stat_scraper.init_driver import get_driver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from stat_scraper.logs.loggers import app_logger
from tqdm import tqdm
import time


def calculate_stat(stats):  # неправильные значения
    app_logger.info('Start CALCULATING collected past stats')
    slices = [3, 5, 10, 15, 20]
    sums = {}
    slice_stats = {}
    for i, stat in enumerate(stats):
        keys = stat.keys()
        for key in keys:
            if key in sums:
                sums[key] += int(stat[key])
            else:
                sums[key] = int(stat[key])
        if i + 1 in slices:
            keys = sums.keys()
            values = sums.values()
            [slice_stats.update({f'{i+1}_last_{key}': value})
             for key, value in zip(keys, values)]
    app_logger.debug(f'Formed slice stats: \n{slice_stats}\n')
    return slice_stats


# та же стат только по разделению дома на выезде
def get_summary_stat(stat_rows, command, limit=10):
    app_logger.info(f'Start received SUMMARY stats for {command}\n')
    summary_stats = []
    for i, stat_row in enumerate(stat_rows):
        if i + 1 > limit:
            app_logger.info(f'Processed {i} events, exit from loop')
            break
        event_stat = {}
        try:
            home_command = stat_row.select(
                'div.event__participant--home')[0].text.strip()
            away_command = stat_row.select(
                'div.event__participant--away')[0].text.strip()
            event_scores = stat_row.select('div.event__scores span')
            first_half_scores = stat_row.select(
                'div.event__part')[0].text.strip('(').strip(')').split('-')
            command_id = 0 if command in home_command else 1
            event_stat['goals_scored'] = event_scores[command_id].text
            event_stat['goals_missed'] = event_scores[command_id-1].text
            event_stat['1half_goals_scored'] = first_half_scores[command_id]
            event_stat['1half_goals_missed'] = first_half_scores[command_id-1]
            event_id = stat_row['id'][4:]
            first_half_url = f'https://www.flashscore.com/match/{event_id}/#match-statistics;1'
            second_half_url = f'https://www.flashscore.com/match/{event_id}/#match-statistics;2'
            app_logger.info(f'STAT ROW {stat_row}')
            app_logger.info(
                f'DETAIL STAT {home_command} {event_scores} {away_command}')
            event_stat.update(get_half_stat(first_half_url, '1st_half'))
            event_stat.update(get_half_stat(second_half_url, '2nd_half'))
            summary_stats.append(event_stat)
        except Exception:
            app_logger.exception(
                f'\nError received data from stat row {command}')
        app_logger.debug(
            f'Formed event stats: \n{event_stat}\n')
    return(calculate_stat(summary_stats))


def get_previous_events(html):
    soup = BeautifulSoup(html, 'lxml')
    app_logger.info(f'Start finding PREV events for {event_date} {url}\n')
    stat_rows = soup.select('div.event__match')
    for stat_row in stat_rows:
        date = stat_row.select('div.event__time')[0].text.split(' ')
        date_parts = date[0].split('.')
        date_format = date_parts[0] + \
            date_parts[1] if len(date) > 1 else '.'.join(date_parts)
        event_date_parts = event_date.split('.')
        event_date_format = event_date_parts[0] + \
            event_date_parts[1] if len(date) > 1 else event_date
        app_logger.debug(
            (f'Getting date {event_date},found date {date},'
                'getting date form {event_date_format},'
                'found date form {date_format}\n'))
        if date_format == event_date_format:
            prev_events = stat_row.find_next_siblings(
                name='div', attrs={'class': 'event__match'})
            app_logger.debu(
                f'Found previous {len(prev_events)} events earlier {event_date}\n')
            return prev_events
    return []


def get_more_events(url, clicks=5):
    driver = get_driver()
    driver.get(url)
    time.sleep(0.5)
    more_event_btn = driver.find_element_by_css_selector('a.event__more')
    more_event_btn.send_keys(Keys.END)
    for i in range(clicks):
        time.sleep(0.5)
        more_event_btn.click()
    html = driver.page_source
    driver.quit()
    return html


print(get_more_events('https://www.flashscore.com/team/nice/YagoQJpq/results/'))


def find_previous_events(url, event_date):  # add selenium click
    html = get_html(url)
    while True:
        prev_events = get_previous_events(html, event_date)
        if len(prev_events) == 0:
            more_html = get_more_events(url)
            prev_events = get_previous_events(more_html, event_date)
        else:
            return prev_events


def get_past_stat(url):
    main_stat = get_main_stat(url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.info(f'Start collect PAST stat data from {url}\n')
    template = 'https://www.flashscore.com{}/results/'
    home_command_url = template.format(soup.select(
        'div.team-text.tname-home a.participant-imglink')[0].attrs[
            'onclick'].split("'")[1])
    away_command_url = template.format(soup.select(
        'div.team-text.tname-away a.participant-imglink')[0].attrs[
            'onclick'].split("'")[1])
    home_prev_events = find_previous_events(home_command_url,
                                            main_stat['home_command'],
                                            main_stat['date'])
    home_past_stat = get_summary_stat(home_prev_events,
                                      main_stat['home_command'])
    # logging
    return home_past_stat


def insert_past_stat(url, filename):
    summary_stat = get_past_stat(url)
    with open(filename, 'w') as file:
        for key in summary_stat:
            file.write('{}: {}\n'.format(key, summary_stat[key]))


def main():  # написать тесты!!!!!!!!!!!
    # insert_past_stat('https://www.flashscore.com/match/C2xXOviA', 'file1.txt')
    # insert_past_stat('https://www.flashscore.com/match/K8BGGGbj', 'file2.txt')
    # insert_past_stat('https://www.flashscore.com/match/baAKFzEd', 'file3.txt')
    # insert_past_stat('https://www.flashscore.com/match/xpMBHdqp', 'file4.txt')
    insert_past_stat(
        'https://www.flashscore.com/match/nNLWvfca', 'invalid.txt')


if __name__ == '__main__':
    main()
