import unittest
from tests.results import expected_dict
from stat_scraper.fs_past_stat_parser import find_previous_events
from stat_scraper.fs_past_stat_parser import get_detail_stat
from stat_scraper.fs_past_stat_parser import calculate_stat


url = 'https://www.flashscore.com/team/nice/YagoQJpq/results/'
result = find_previous_events(url, 'Nice', 'Ligue 1', '04.12.2019')
print(len(result))
for stat_row in result:
    event_id = stat_row['id'][4:]
    first_half_url = f'https://www.flashscore.com/match/{event_id}/#match-statistics;1'
    print(first_half_url)

# https://www.flashscore.com/match/nNLWvfca/#match-statistics;0 протестировать поведение на некорректном событии


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
        self.assertEqual(result, expected_dict)

    def test_find_prev_events(self):
        url = 'https://www.flashscore.com/team/nice/YagoQJpq/results/'
        result = len(find_previous_events(
            url, 'Nice', 'Ligue 1', '04.12.2019'))
        self.assertEqual(result, 22)

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
