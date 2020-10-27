import requests

def get_city_info(city, state):
    query = {'action': 'query', 'format': 'json', 'titles': f'{city},_{state}', 'prop': 'extracts', 'exintro': '', 'explaintext': '', 'redirects': ''}
    url = 'https://en.wikipedia.org/w/api.php?'

    try:
        data = requests.get(url, params=query).json()
        page_data = data['query']['pages']
        page_id = list(page_data.keys())
        return (page_id[0], page_data[f'{page_id[0]}']['extract'])
    except KeyError as err:
        return 'KeyError', err
    except requests.exceptions.ConnectionError as err:
        return 'ConnectionError', err


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


