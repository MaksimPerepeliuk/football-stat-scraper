from stat_scraper.fs_past_stat_parser import get_past_stat


urls = [
    'https://www.flashscore.com/match/EF8mdLtQ',
    'https://www.flashscore.com/match/WxvhMBVB',
    'https://www.flashscore.com/match/ncdnSOY3',
    'https://www.flashscore.com/match/8OrmpJeh',
    'https://www.flashscore.com/match/Qo0YDWlr',
    'https://www.flashscore.com/match/pn7zSXon',
    'https://www.flashscore.com/match/8C6mIsTe',
    'https://www.flashscore.com/match/GjabGyLf',
    'https://www.flashscore.com/match/xdS9x8T6',
    'https://www.flashscore.com/match/xfTkwU6A'
]


def write_file(filename, data):
    with open(filename, 'a') as file:
        file.write(f'{data}\n\n\n\n')


def run_parse(urls, filename):
    for url in urls:
        try:
            write_file(filename, get_past_stat(url))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    run(urls, 'smoke_test_result.txt')


# [Running] /usr/bin/python3 "/home/max/Projects/football-stat-scraper/tests/past_stat_smoke_test.py"
# Traceback (most recent call last):
#   File "/home/max/Projects/football-stat-scraper/tests/past_stat_smoke_test.py", line 28, in <module>
#     run()
#   File "/home/max/Projects/football-stat-scraper/tests/past_stat_smoke_test.py", line 25, in run
#     write_file('smoke_test_result.txt', get_past_stat(url))
#   File "/home/max/Projects/football-stat-scraper/stat_scraper/fs_past_stat_parser.py", line 136, in get_past_stat
#     main_stat = get_main_stat(url)
#   File "/home/max/Projects/football-stat-scraper/stat_scraper/fs_live_stat_parser.py", line 76, in get_main_stat
#     main_stat['round_num'] = championate_info.split(
# IndexError: list index out of range

# [Done] exited with code=1 in 945.824 seconds
