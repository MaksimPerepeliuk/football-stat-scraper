from events_urls_parser import driver  # в отдельный модуль
import time


def get_stat(url):
    driver.get(url)
    time.sleep(0.5)
    championate_info = driver.find_elements_by_css_selector(
        'span.description__country')[0].text
    country = championate_info.split(':')[0]
    championate = championate_info.split(':')[1].split('-')[0]
    round_num = championate_info.split(':')[1].split('-')[1]
    date = driver.find_element_by_css_selector(
        'div#utime').text.split(' ')[0]
    home_command = driver.find_elements_by_css_selector(
        'div.team-text.tname-home a.participant-imglink')[0].text
    away_command = driver.find_elements_by_css_selector(
        'div.team-text.tname-away a.participant-imglink')[0].text
    result_score = driver.find_elements_by_css_selector(
        'div#event_detail_current_result')[0].text.strip()
    goal_time = driver.find_elements_by_css_selector(
        'div.icon-box.soccer-ball')
    print(len(goal_time))


get_stat('https://www.flashscore.com/match/C2xXOviA')
