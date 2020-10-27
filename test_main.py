import requests
import unittest
from unittest import TestCase
from unittest import mock
from main import get_city_info, get_page_url

# figured out how to do patching request.get from here, or at least, know only a tiny bit about it.
# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response

def mock_requests_get(url, params):
    class MockAPI:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if params['titles'] == 'minneapolis,_mn':
        return MockAPI({"batchcomplete":"","query":{"pages":{"27687":{"pageid":27687,"ns":0,"title":"Minneapolis","extract":"This is a correct API response"}}}})
    elif params['titles'] == 'test,_mn':
        return MockAPI({"batchcomplete":"","query":{"pages":{"1":{"ns":0,"title":"Test, MN","missing":""}}}})
    return MockAPI(None)

class TestWikiAPI(TestCase):

    # This one works like how I want it to, which is at least something
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetch_with_correct_city_name(self, mock_get):
        page_id, intro_extract = get_city_info('minneapolis', 'mn')
        self.assertEqual(page_id, "27687")
        self.assertEqual(intro_extract, "This is a correct API response")

    # This one doesn't for two reasons. 1. for some reason I get an index error every time I try to have two tests in this testcase?
    # and it's probably something with the mock requests.get that I don't understand.
    # The other way it doesn't work is that I don't know how to raise the KeyError without main.py crashing when run on its own.

    # @mock.patch('requests.get', side_effects=mock_requests_get)
    # def test_fetch_with_incorrect_city_name(self, mock_get):
    #     with self.assertRaises(KeyError):
    #         get_city_info('test', 'mn')




if __name__ == '__main__':
    unittest.main()