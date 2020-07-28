from stat_scraper.fs_live_stat_parser import get_main_stat, get_half_stat
import unittest


main_stat = {
    'country': 'FRANCE',
    'championate': 'Ligue 1',
    'round_num': 'Round 11',
    'date': '30.10.2016',
    'home_command': 'Nice',
    'away_command': 'Nantes',
    'result_score': '4-1',
    'goal_minutes': '9-27-47-60-65',
}

first_half_stat = {
    '1st_half_ball_possession_home': 64,
    '1st_half_ball_possession_away': 36,
    '1st_half_goal_attempts_home': 9,
    '1st_half_goal_attempts_away': 9,
    '1st_half_shots_on_goal_home': 5,
    '1st_half_shots_on_goal_away': 1,
    '1st_half_shots_off_goal_home': 2,
    '1st_half_shots_off_goal_away': 6,
    '1st_half_blocked_shots_home': 2,
    '1st_half_blocked_shots_away': 2,
    '1st_half_corner_kicks_home': 0,
    '1st_half_corner_kicks_away': 3,
    '1st_half_offsides_home': 1,
    '1st_half_offsides_away': 2,
    '1st_half_goalkeeper_saves_home': 1,
    '1st_half_goalkeeper_saves_away': 3,
    '1st_half_fouls_home': 5,
    '1st_half_fouls_away': 9,
    '1st_half_yellow_cards_home': 0,
    '1st_half_yellow_cards_away': 2,
}

second_half_stat = {
    '2nd_half_ball_possession_home': 62,
    '2nd_half_ball_possession_away': 38,
    '2nd_half_goal_attempts_home': 3,
    '2nd_half_goal_attempts_away': 7,
    '2nd_half_shots_on_goal_home': 2,
    '2nd_half_shots_on_goal_away': 3,
    '2nd_half_shots_off_goal_home': 1,
    '2nd_half_shots_off_goal_away': 3,
    '2nd_half_blocked_shots_home': 0,
    '2nd_half_blocked_shots_away': 1,
    '2nd_half_corner_kicks_home': 2,
    '2nd_half_corner_kicks_away': 1,
    '2nd_half_offsides_home': 1,
    '2nd_half_offsides_away': 3,
    '2nd_half_goalkeeper_saves_home': 2,
    '2nd_half_goalkeeper_saves_away': 0,
    '2nd_half_fouls_home': 7,
    '2nd_half_fouls_away': 9,
    '2nd_half_yellow_cards_home': 1,
    '2nd_half_yellow_cards_away': 1,
}


class LiveStatParser(unittest.TestCase):
    url = 'https://www.flashscore.com/match/hjDXGPqp/'

    def test_main_stat(self):
        result = get_main_stat(self.url)
        self.assertEqual(result, main_stat)

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
