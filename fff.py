from stat_scraper.fs_past_stat_parser import find_previous_events
from stat_scraper.fs_past_stat_parser import get_detail_stat
from stat_scraper.fs_past_stat_parser import calculate_stat


def get_testing_object():
    res = []
    for i in range(10):
        obj = {}
        obj['1st_half_ball_possession_home'] = 10
        obj['1st_half_ball_possession_away'] = 20
        obj['1st_half_goal_attempts_home'] = 30
        obj['1st_half_goal_attempts_away'] = 40
        obj['2nd_half_ball_possession_home'] = 10
        obj['2nd_half_ball_possession_away'] = 20
        obj['2nd_half_goal_attempts_home'] = 30
        obj['2nd_half_goal_attempts_away'] = 40
        res.append(obj)
    return res


calc = get_testing_object()
calc[4]['2nd_half_red_card_home'] = 1
calc[4]['2nd_half_red_card_away'] = 0

print(calculate_stat(calc))
