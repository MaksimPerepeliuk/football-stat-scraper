from logs.loggers import debug_log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chromedriver_path = '/home/max/Projects/tmp/chromedriver'
driver = webdriver.Chrome(options=chrome_options,
                          executable_path=chromedriver_path)


def make_url_event_stat(events_id):
    template = 'https://www.flashscore.ru/match/{}'
    result_urls = []
    for id in events_id:
        result_urls.append(template.format(id[4:]))
    return result_urls


def get_events_urls(url):
    driver.get(url)
    debug_log(f'Open page - {url}')
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
        debug_log('All events open')

    debug_log('start getting events line')
    time.sleep(1)
    events_lines = driver.find_elements_by_css_selector(
        'div.sportName div.event__match')
    events_id = [event.get_attribute('id') for event in events_lines]
    debug_log(f'got {len(events_id)} events id')
    driver.close()
    return make_url_event_stat(events_id)


urls = get_events_urls(
    'https://www.flashscore.ru/football/germany/bundesliga-2017-2018/results/')


print(len(urls))
print(urls)
