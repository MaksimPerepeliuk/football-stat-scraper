from logs.loggers import debug_log, err_log, info_log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from db_manager import insert_into_events_urls
from tqdm import tqdm
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chromedriver_path = '/home/max/Projects/tmp/chromedriver'
driver = webdriver.Chrome(options=chrome_options,
                          executable_path=chromedriver_path)


def normalize_list_urls(urls):
    stop_strings = ['', ' ']
    clear_urls = list(filter(lambda url: url not in stop_strings, urls))
    return [url.strip() for url in clear_urls]


def get_country_urls():
    file_content = open('foot_stat_scraper/country_urls.txt').read()
    return normalize_list_urls(file_content.split(', '))


def write_url_in_file(url):
    with open('foot_stat_scraper/champ_urls.txt', 'a') as file:
        file.write(f'{url}, ')


def make_file_champ_urls(country_urls):
    for url in tqdm(country_urls):
        archive_url = url + 'archive/'
        driver.get(archive_url)
        time.sleep(1)
        champs_by_years = driver.find_elements_by_css_selector(
            'div.leagueTable__season div.leagueTable__seasonName')
        for i, champ in enumerate(champs_by_years[:3]):
            champ_text = champ.find_element_by_css_selector('a').text
            season = champ_text.split(' ')[1]
            country = driver.find_element_by_css_selector(
                'h2.tournament').text.split('\n')[1]
            try:
                champ_url = champ.find_element_by_css_selector(
                    'a').get_attribute('href')
                debug_log(f'received url - {champ_url} by {country} {season}')
                write_url_in_file(champ_url)
            except Exception:
                err_log('\nError getting or writing in file element')


def make_url_event(events_id):
    template = 'https://www.flashscore.ru/match/{}'
    result_urls = []
    for id in events_id:
        result_urls.append(template.format(id[4:]))
    return result_urls


def get_events_urls(champoinate_url):
    driver.get(champoinate_url)
    debug_log(f'Open page - {champoinate_url}')
    time.sleep(1)
    more_event = driver.find_element_by_css_selector('a.event__more')
    more_event.send_keys(Keys.END)
    try:
        for i in range(1, 11):
            debug_log(f'get events page #{i}')
            time.sleep(2)
            more_event.click()
            if i > 8:
                debug_log('too many pages open')
    except Exception:
        debug_log('All events open\n')
    time.sleep(1)
    events_lines = driver.find_elements_by_css_selector(
        'div.sportName div.event__match')
    events_id = [event.get_attribute('id') for event in events_lines]
    return make_url_event(events_id)


def main(champ_urls):
    count_records = 0
    for champ_url in tqdm(champ_urls):
        time.sleep(2)
        try:
            events_urls = normalize_list_urls(
                get_events_urls(champ_url + 'results/'))
            info_log(f'Received {len(events_urls)} events urls')
            [insert_into_events_urls(event_url) for event_url in (events_urls)]
            info_log(f'Record in db {len(events_urls)} urls ')
            count_records += len(events_urls)
            info_log(f'Total number of records = {count_records}\n')
        except Exception:
            err_log('\nreceive or record error')
    driver.quit()


if __name__ == '__main__':
    champ_urls = champ_urls = open(
        'foot_stat_scraper/champ_urls.txt').read().split(', ')
    main(champ_urls)
