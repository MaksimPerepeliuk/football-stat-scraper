import sys
sys.path.append('/home/max/Projects/football-stat-scraper/foot_stat_scraper')
from fs_live_stat_parser import get_main_stat, get_half_stat
import unittest
from results import main_stat, first_half_stat, second_half_stat


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
