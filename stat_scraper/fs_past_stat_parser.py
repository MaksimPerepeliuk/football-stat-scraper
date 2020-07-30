from stat_scraper.fs_live_stat_parser import get_html, get_main_stat
from stat_scraper.fs_live_stat_parser import get_half_stat
from stat_scraper.init_driver import get_driver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from stat_scraper.logs.loggers import app_logger
from tqdm import tqdm
import time


def calculate_stat(stats):
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


def find_position_events(stats, command, position):
    position_stats = []
    for stat in stats:
        home_position = stat.select('div.event__participant--home')[0].text
        away_position = stat.select('div.event__participant--away')[0].text
        target = home_position if position == 'home' else away_position
        if target == command:
            position_stats.append(stat)
    return position_stats


# та же стат только по разделению дома на выезде
def get_summary_stat(stat_rows, command, position, dependence='position', limit=5):
    app_logger.info(f'Start received SUMMARY stats for {command}\n')
    stat_rows = (find_position_events(stat_rows, command, position)
                 if dependence == 'position' else stat_rows)
    summary_stats = []
    for i, stat_row in enumerate(stat_rows[:limit]):
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
            app_logger.info(
                f'DETAIL STAT {home_command} {event_scores} {away_command}')
            event_stat.update(get_half_stat(
                first_half_url, '1st_half', command_id))
            event_stat.update(get_half_stat(
                second_half_url, '2nd_half', command_id))
            summary_stats.append(event_stat)
        except Exception:
            app_logger.exception(
                f'\nError received data from stat row {command}')
        app_logger.debug(
            f'Formed event stats: \n{event_stat}\n')
    return(calculate_stat(summary_stats))


def get_more_events(url, clicks=10):
    driver = get_driver()
    driver.get(url)
    time.sleep(1)
    more_event_btn = driver.find_element_by_css_selector('a.event__more')
    more_event_btn.send_keys(Keys.END)
    app_logger.info(f'Start CLICKING to show more btn on {url} page')
    for i in range(clicks):
        try:
            time.sleep(1)
            more_event_btn.click()
        except Exception:
            app_logger.exception('Button show more events not found url {url}')
            html = driver.page_source
            driver.quit()
            return html
    html = driver.page_source
    driver.quit()
    return html


def find_previous_events(url, event_date):
    html = get_more_events(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.info(f'Start finding PREV events for {event_date}\n')
    stat_rows = soup.select('div.event__match')
    last_date = stat_rows[-1].select('div.event__time')[0].text.split(' ')[0]
    app_logger.info(f'LAST date in received stat rows = {last_date}\n')
    for stat_row in stat_rows:
        date = stat_row.select('div.event__time')[0].text.split(' ')
        date_parts = date[0].split('.')
        date_format = date_parts[0] + \
            date_parts[1] if len(date) > 1 else '.'.join(date_parts)
        event_date_parts = event_date.split('.')
        event_date_format = event_date_parts[0] + \
            event_date_parts[1] if len(date) > 1 else event_date
        if date_format == event_date_format:
            prev_events = stat_row.find_next_siblings(
                name='div', attrs={'class': 'event__match'})
            app_logger.debug(
                f'Found previous {len(prev_events)} events earlier {event_date}\n')
            return prev_events
    return []


def add_type_command(stats, type_command):
    items = stats.items()
    result = {}
    for key, value in items:
        result[f'{type_command}_' + key] = value
    return result


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
    home_prev_events = find_previous_events(home_command_url, main_stat['date'])
    away_prev_events = find_previous_events(away_command_url, main_stat['date'])
    past_stat = {}
    home_past_stat = add_type_command(get_summary_stat(
        home_prev_events, main_stat['home_command'], 'home'), 'HOME')
    away_past_stat = add_type_command(get_summary_stat(
        away_prev_events, main_stat['away_command'], 'away'), 'AWAY')
    past_stat.update(home_past_stat)
    past_stat.update(away_past_stat)
    app_logger.debug(f'Formed PAST STAT: \n{past_stat}\n')
    return past_stat


# def insert_past_stat(url, filename):
#     summary_stat = get_past_stat(url)
#     with open(filename, 'w') as file:
#         for key in summary_stat:
#             file.write('{}: {}\n'.format(key, summary_stat[key]))


def main():  # написать тесты!!!!!!!!!!!
    # get_past_stat('https://www.flashscore.com/match/C2xXOviA')
    # insert_past_stat('https://www.flashscore.com/match/K8BGGGbj', 'file2.txt')
    # insert_past_stat('https://www.flashscore.com/match/baAKFzEd', 'file3.txt')
    get_past_stat('https://www.flashscore.com/match/xpMBHdqp')
    # get_past_stat('https://www.flashscore.com/match/nNLWvfca', 'invalid.txt')


if __name__ == '__main__': # каково буде т поведение при try на этом этапе
    main()
