def convert_urls():
    urls = open('foot_stat_scraper/urls/now_goal_urls.txt').read().split(', ')
    template = 'http://data.nowgoal.group/3in1odds/{}'
    new_urls = []
    for url in urls:
        tail_url = '3_' + url.split('/')[-1]
        new_urls.append(template.format(tail_url))
    unique_new_urls = list(set(new_urls))
    return unique_new_urls
