import unittest
from power_of_10 import rankings, exceptions

class GetRankings(unittest.TestCase):
    def test_all_search_fields_filled(self):
        ranks = rankings.get_rankings(year=2016, gender='M', age_group='U20', event='400', region='london')
        self.assertEqual(len(ranks), 64)

    def test_all_fields_but_region(self):
        ranks = rankings.get_rankings(year=2016, gender='M', age_group='U20', event='400')
        self.assertEqual(len(ranks), 427)

    def test_year_gender_age_group(self):
        with self.assertRaises(TypeError):
            rankings.get_rankings(year=2016, gender='M', age_group='U20')

    def test_future_year(self):
        ranks = rankings.get_rankings(year=2030, gender='M', age_group='U20', event='400')
        self.assertEqual(ranks, [])

    def test_invalid_year(self):
        ranks = rankings.get_rankings(year='gsgs', gender='M', age_group='U20', event='400')
        self.assertEqual(ranks, [])

    def test_invalid_region(self):
        with self.assertRaises(exceptions.QueryError):
            rankings.get_rankings(year=2016, region='japan', gender='M', age_group='U20', event='400')

    def test_invalid_gender(self):
        ranks = rankings.get_rankings(year=2016, gender='S', age_group='U20', event='400')
        self.assertEqual(ranks, [])

    def test_invalid_age_group(self):
        ranks = rankings.get_rankings(year=2016, gender='M', age_group='U99', event='400')
        self.assertEqual(ranks, [])

    def test_invalid_event(self):
        ranks = rankings.get_rankings(year=2016, gender='M', age_group='U20', event='123')
        self.assertEqual(ranks, [])

    def test_empty_search(self):
        with self.assertRaises(TypeError):
            rankings.get_rankings()


if __name__ == '__main__':
    unittest.main()