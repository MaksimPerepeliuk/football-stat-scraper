import unittest
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


calc_stat = {
    '3_last_1st_half_ball_possession_home': 30,
    '3_last_1st_half_ball_possession_away': 60,
    '3_last_1st_half_goal_attempts_home': 90,
    '3_last_1st_half_goal_attempts_away': 120,
    '3_last_2nd_half_ball_possession_home': 30,
    '3_last_2nd_half_ball_possession_away': 60,
    '3_last_2nd_half_goal_attempts_home': 90,
    '3_last_2nd_half_goal_attempts_away': 120,
    '5_last_1st_half_ball_possession_home': 50,
    '5_last_1st_half_ball_possession_away': 100,
    '5_last_1st_half_goal_attempts_home': 150,
    '5_last_1st_half_goal_attempts_away': 200,
    '5_last_2nd_half_ball_possession_home': 50,
    '5_last_2nd_half_ball_possession_away': 100,
    '5_last_2nd_half_goal_attempts_home': 150,
    '5_last_2nd_half_goal_attempts_away': 200,
    '5_last_2nd_half_red_card_home': 1,
    '5_last_2nd_half_red_card_away': 0,
    '10_last_1st_half_ball_possession_home': 100,
    '10_last_1st_half_ball_possession_away': 200,
    '10_last_1st_half_goal_attempts_home': 300,
    '10_last_1st_half_goal_attempts_away': 400,
    '10_last_2nd_half_ball_possession_home': 100,
    '10_last_2nd_half_ball_possession_away': 200,
    '10_last_2nd_half_goal_attempts_home': 300,
    '10_last_2nd_half_goal_attempts_away': 400,
    '10_last_2nd_half_red_card_home': 1,
    '10_last_2nd_half_red_card_away': 0
}


class LiveStatParser(unittest.TestCase):
    url = 'https://www.flashscore.com/match/hjDXGPqp/'

    def test_calculate_stat(self):
        calc = get_testing_object()
        calc[4]['2nd_half_red_card_home'] = 1
        calc[4]['2nd_half_red_card_away'] = 0
        result = calculate_stat()
        self.assertEqual(result, calc_stat)

    def test_first_half_stat(self):
        first_half_url = self.url + '#match-statistics;1'
        result = get_half_stat(first_half_url, '1st_half')
        self.assertEqual(result, first_half_stat)

    def test_second_half_stat(self):
        second_half_url = self.url + '#match-statistics;2'
        result = get_half_stat(second_half_url, '2nd_half')
        self.assertEqual(result, second_half_stat)


if __name__ == '__main__':
    unittest.main()
