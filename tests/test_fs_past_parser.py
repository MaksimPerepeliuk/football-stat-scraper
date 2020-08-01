import unittest
from tests.expected_values import expected_calc_dict, expected_summary_values
from stat_scraper.fs_past_stat_parser import get_summary_stat
from stat_scraper.fs_past_stat_parser import get_previous_events
from stat_scraper.fs_past_stat_parser import calculate_stat


class LiveStatParser(unittest.TestCase):

    def get_testing_dict(self):
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
        res[4]['2nd_half_red_card_home'] = 1
        res[4]['2nd_half_red_card_away'] = 0
        return res

    def test_calculate_stat(self):
        testing_dict = self.get_testing_dict()
        result = calculate_stat(testing_dict)
        self.assertEqual(result, expected_calc_dict)

    def test_get_summary_stat(self):
        url = 'https://www.flashscore.com/team/nice/YagoQJpq/results/'
        result = get_summary_stat(
            get_previous_events(url, '29.09.2018', 3), 'Nice')
        self.assertEqual(list(result.values())[:5], expected_summary_values)


if __name__ == '__main__':
    unittest.main()
