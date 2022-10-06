from requests import Session
from requests.exceptions import SSLError
import json


def get_coin_api_value(money_id: int) -> float:
    API_PATH = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    try:
        response = session.get(
            API_PATH, params={'id': str(money_id), 'convert': 'EUR'})
        data = json.loads(response.text)
    except SSLError:
        return 0.0
    except:
        return 0.0
    
    try:
        price = float(
            data['data'][str(money_id)]['quote']['EUR']['price'])
    except (KeyError, ValueError):
        return 0.0

    return price

# base_url = 'https://pro-api.coinmarketcap.com/v2/'
# url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/listings/latest'

# parameters = {
#   # 'id':'1',
#   # 'start': '1',
#   # 'id': 9840,
#   # 'limit':'5000',
#   # 'id': '9840',
#   # 'convert':'EUR'
# }

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '78bf3faa-4a1a-405c-bf13-d79d90a491da',
}

session = Session()
session.headers.update(headers)
    

# print('eokez')

# pathi = 'https://pro-api.coinmarketcap.com/v1/'

# # rourou = pathi  + 'cryptocurrency/' + 'quotes/latest'
# rourou = pathi  + 'cryptocurrency/' + 'map'


# print('aa:', str(rourou))
# response = session.get(str(rourou), params=parameters)
# # print(response.text)
# data = json.loads(response.text)
# # print('oulalla', len(data['data']))
# with open('api_map.json', 'w') as f:
#     json.dump(data, f, indent=4)
