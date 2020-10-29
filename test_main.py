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
        # page_id, intro_extract = get_city_info('minneapolis', 'mn')
        error, data = get_city_info('minneapolis', 'mn')
        page_id = data.page_id
        intro_extract = data.contents
        self.assertIsNone(error)
        self.assertEqual(page_id, "27687")
        self.assertEqual(intro_extract, "This is a correct API response")

    # This one doesn't for two reasons. 1. for some reason I get an index error every time I try to have two tests in this testcase?
    # and it's probably something with the mock requests.get that I don't understand. - no, your mock is working as intended. 

    # The other way it doesn't work is that I don't know how to raise the KeyError without main.py crashing when run on its own.
    #     -- main.py can use a try-except if necessary.   But I don't think you should let the KeyError be thrown.  

    # your code is not raising a key error. So the test is failing. the test would pass if get_city_info raised a key error. 
    # suggest avoiding raising key errors. why do you get key errors? either place not found, which the app needs to know so it can 
    # display an appropriate page to the user.   
    # 
    # Or the format of JSON data from wikipedia is different to expected or the code 
    # that processes the JSON has a bug. Either one of these - log error info and return a general error message, this is something 
    # a programmer needs to fix. 
    @mock.patch('requests.get', side_effects=mock_requests_get)
    def test_fetch_with_incorrect_city_name(self, mock_get):
        error, data = get_city_info('test', 'mn')
        self.assertEqual('Not found', error)    # key error isn't very descriptive. Can you re-work the API call code to figure out if 
        # the place is not found and return something that implies not found, instead of key error? 
        self.assertIsNone(data) 



if __name__ == '__main__':
    unittest.main()