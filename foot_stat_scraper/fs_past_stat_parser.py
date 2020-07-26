from fs_live_stat_parser import get_html, get_main_stat, get_half_stat
from bs4 import BeautifulSoup
from logs.loggers import app_logger


def calculate_stat(stats): # неправильные значения
    app_logger.debug('Start CALCULATING collected past stats')
    slices = [3, 5, 10, 15, 20]
    sums = {}
    slice_stats = {}
    for i, stat in enumerate(stats):
        if i + 1 in slices:
            keys = sums.keys()
            values = sums.values()
            [slice_stats.update({f'{i+1}_last_{key}': value})
             for key, value in zip(keys, values)]
            app_logger.info(f'Make SLICE stats last {i} previous events')
        keys = stat.keys()
        for key in keys:
            if key in sums:
                sums[key] += int(stat[key])
            else:
                sums[key] = int(stat[key])
    app_logger.debug(f'\n{slice_stats}')


def get_detail_stat(stat_rows, command, championate, limit=3):
    app_logger.debug(f'Start calculate stats for {command}')
    summary_stats = []
    for i, stat_row in enumerate(stat_rows):
        if i > limit:
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
            event_stat.update(get_half_stat(first_half_url, '1st_half'))
            event_stat.update(get_half_stat(second_half_url, '2nd_half'))
            summary_stats.append(event_stat)
            app_logger.debug(
                f'Add event #{i} with {len(event_stat)} keys stat in summary stat')
        except Exception:
            app_logger.exception(
                f'\nError received data from stat row {command}')
    calculate_stat(summary_stats)


def get_past_command_stat(url, command, championate, event_date):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.debug(
        f'Start collect COMMAND stat data from {url} command {command}')
    stat_rows = soup.select('div.event__match')
    for stat_row in stat_rows:
        date = stat_row.select('div.event__time')[0].text.split(' ')
        date_parts = event_date.split('.')
        date_format = date_parts[0] + \
            date_parts[1] if len(date) > 1 else '.'.join(date_parts)
        event_date_parts = event_date.split('.')
        event_date_format = event_date_parts[0] + \
            event_date_parts[1] if len(date) > 1 else event_date
        if date_format == event_date_format:
            prev_events = stat_row.find_next_siblings(
                name='div', attrs={'class': 'event__match'})
            return get_detail_stat(prev_events, command, championate)


def get_summary_past_stat(url):
    main_stat = get_main_stat(url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    app_logger.debug(f'Start collect SUMMARY stat data from {url}')
    template = 'https://www.flashscore.com{}/results/'
    home_command_url = template.format(soup.select(
        'div.team-text.tname-home a.participant-imglink')[0].attrs[
            'onclick'].split("'")[1])
    away_command_url = template.format(soup.select(
        'div.team-text.tname-away a.participant-imglink')[0].attrs[
            'onclick'].split("'")[1])
    home_past_stat = get_past_command_stat(
        home_command_url, main_stat['home_command'],
        main_stat['championate'], main_stat['date'])


def insert_past_stat(url):
    summary_stat = get_summary_past_stat(url)


def main():
    insert_past_stat('https://www.flashscore.com/match/C2xXOviA')


main()
