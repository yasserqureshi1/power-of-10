import unittest
from power_of_10 import athletes, exceptions


class FindAthletes(unittest.TestCase):
    def test_common_firstname(self):
        with self.assertRaises(exceptions.BroadQueryError):
            athletes.search_athletes(firstname='John')

    def test_common_surname(self):
        with self.assertRaises(exceptions.BroadQueryError):
            athletes.search_athletes(surname='smith')

    def test_large_club(self):
        with self.assertRaises(exceptions.BroadQueryError):
            athletes.search_athletes(club='sutton')

    def test_rare_firstname(self):
        aths = athletes.search_athletes(firstname='Yasser')
        self.assertEqual(len(aths), 2)

    def test_rare_surname(self):
        aths = athletes.search_athletes(surname='Qureshi')
        self.assertEqual(len(aths), 13)

    def test_specific_person(self):
        ath = athletes.search_athletes(firstname='Yasser', surname='Qureshi')
        ath1 = [{'firstname': 'Yasser', 'surname': 'Qureshi', 'track': 'U23', 'road': 'U23', 'xc': 'U23', 'sex': 'M', 'club': 'Sutton & District', 'athlete_id': '522041'}]
        self.assertEqual(ath, ath1)

    def test_no_search(self):
        with self.assertRaises(exceptions.QueryError):
            athletes.search_athletes()

    def test_non_exisiting_athlete(self):
        with self.assertRaises(exceptions.BroadQueryError):
            athletes.search_athletes('gsgbiis')


class TestGetAthletes(unittest.TestCase):
    def test_specific_athlete_id(self):
        ath = athletes.get_athlete(athlete_id=522041)
        self.assertEqual(ath['club'], 'Sutton & District')

    def test_non_existing_athlete_id(self):
        with self.assertRaises(exceptions.QueryError):
            athletes.get_athlete(athlete_id=111111)

    def test_coach_athlete_id(self):
        ath = athletes.get_athlete(athlete_id=94998)
        self.assertEqual(ath['club'], 'Blackheath & Bromley')

    def test_random_string(self):
        with self.assertRaises(exceptions.QueryError):
            athletes.get_athlete(athlete_id='gerogiegn')

    def test_famous_athlete(self):
        ath = athletes.get_athlete(athlete_id=46473)
        self.assertEqual(ath['club'], 'Blackheath & Bromley')


if __name__ == '__main__':
    unittest.main()