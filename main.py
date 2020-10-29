import requests
import logging
from dataclasses import dataclass

def main():
    error, data = get_city_info('Minneapolis', 'MN')
    if data:
        print(data.page_id)
        print(data.contents)   # or whatever 
    if error:
        if error == 'Not found':
            print('sorry not found')    
        else:
            print('sorry cant connect to wikipedia')


@dataclass   # you don't need a class but if you are returning several pieces of data a class is handy 
class WikiResponse:
    page_id: int
    contents: str


def get_city_info(city, state):

    # return a tuple of error, data.  
    # If there's an error, return (error, None).  
    # If there's no error and data, return (None, data)

    query = {
        'action': 'query', 
        'format': 'json', 
        'titles': f'{city},_{state}', 
        'prop': 'extracts', 
        'exintro': '', 
        'explaintext': '', 
        'redirects': ''}
    
    url = 'https://en.wikipedia.org/w/api.php?'

    try:
        data = requests.get(url, params=query).json()
        page_data = data['query']['pages']
        page_id = list(page_data.keys())
        from pprint import pprint
        pprint(data)
        # todo make sure you have at least one result
        # you can tell the difference between result and not result by looking at the data in the JSON
        first_page_id = page_id[0]   # i'm kinda guessing on the variable names
        # this line has a key error, there's no 'extract' if no page found.
        # You can check for this instead of letting the key error or index error be raised
        first_page_data = page_data[f'{page_id[0]}']['extract']    
        wiki_respponse = WikiResponse(first_page_id, first_page_data)
        return None, wiki_respponse

    except ValueError as err:
        # response.json() raises this if response is not valid JSON 
        logging.error(err)   # customize logging as appropriate 
        return 'Not a JSON response', None
    except (KeyError, IndexError) as err:
        logging.error('key error: ' + str(err))   # or whatever would be useful
        return 'Unexpected JSON format', None
    except requests.exceptions.RequestException as err:  # there's a lot of other possible ways to not work https://requests.readthedocs.io/en/master/_modules/requests/exceptions/
        logging.error(err)
        return 'ConnectionError', None



def get_page_url(page_id):
    query = {'action': 'query', 'prop': 'info', 'pageids': f'{page_id}', 'inprop': 'url', 'format': 'json'}
    url = 'https://en.wikipedia.org/w/api.php?'

    try:
        data = requests.get(url, params=query).json()
        return (data['query']['pages'][f'{page_id}']['fullurl'])
    except KeyError as err:
        return False

# city = 'test'
# state = 'mn'

# test1, test2 = get_city_info(city, state)
# print(test1)
# print(test2)

# test3 = get_page_url(test2)
# print(test3)

main()
