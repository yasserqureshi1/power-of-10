import unittest
from power_of_10 import results, exceptions


class SearchEvent(unittest.TestCase):
    def test_regular_search(self):
        res = results.search_event(event=400, venue='Lee Valley', date_from='1-Jan-2016', date_to='20-Feb-2016', year=2016, terrain='track/10k/hm/mar/xc')
        self.assertEqual(len(res), 9)

    def test_regular_search_2(self):
        res = results.search_event(event=200, venue='croydon', date_from='1-Jul-2014', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')
        self.assertEqual(len(res), 3)

    def test_invalid_event(self):
        with self.assertRaises(exceptions.QueryError):
            results.search_event(event=10, date_from='1-Jul-2014', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')

    def test_invalid_meeting(self):
        with self.assertRaises(exceptions.QueryError):
            results.search_event(meeting='ffds', date_from='1-Jul-2014', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')

    def test_invalid_venue(self):
        with self.assertRaises(exceptions.QueryError):
            results.search_event(venue='fsfsd', date_from='1-Jul-2014', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')

    def test_invalid_date_from(self):
        with self.assertRaises(exceptions.QueryError):
            results.search_event(date_from='gsfgsf', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')

    def test_invalid_date_to(self):
        res = results.search_event(date_to='gsfgsf', date_from='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')
        self.assertEqual(len(res), 16)
    
    def test_invalid_year(self):
        res = results.search_event(venue='Lee Valley', year=2014, terrain='track/10k/hm/mar/xc')
        self.assertEqual(len(res), 59)

    def test_invalid_meeting_type(self):
        with self.assertRaises(KeyError):
            results.search_event(meeting_type='fsfsdfs', year=2014, terrain='track/10k/hm/mar/xc')

    def test_invalid_terrain(self):
        with self.assertRaises(KeyError):
            results.search_event(date_from='1-Jul-2014', date_to='20-Aug-2014', year=2014, terrain='sdfsd')

    def test_large_query(self):
        with self.assertRaises(exceptions.QueryError):
            results.search_event(date_from='1-Jan-2014', date_to='20-Aug-2014', year=2014, terrain='track/10k/hm/mar/xc')


class GetResults(unittest.TestCase):
    def test_valid_meeting_id(self):
        res = results.get_results(105700)
        self.assertEqual(len(res['results']), 7)

    def test_invalid_meeting_id(self):
        with self.assertRaises(exceptions.QueryError):
            results.get_results(111111111)

if __name__ == '__main__':
    unittest.main()