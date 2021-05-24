import unittest
from power_of_10 import coaches, exceptions

class FindCoaches(unittest.TestCase):
    def test_firstname(self):
        coach = coaches.search_coaches(firstname='John')
        self.assertEqual(len(coach), 225)

    def test_surname(self):
        coach = coaches.search_coaches(surname='smith')
        self.assertEqual(len(coach), 95)

    def test_club(self):
        coach = coaches.search_coaches(club='sutton')
        self.assertEqual(len(coach), 41)

    def test_specific_person(self):
        coach = coaches.search_coaches(firstname='alex', surname='abbott', club='sutton')
        self.assertEqual(coach, '380620')

    def test_no_search(self):
        with self.assertRaises(exceptions.QueryError):
            coaches.search_coaches()

    def test_non_exisiting_athlete(self):
        with self.assertRaises(exceptions.QueryError):
            coaches.search_coaches('ouoiubui')

if __name__ == '__main__':
    unittest.main()