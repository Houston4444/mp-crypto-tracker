from requests import Session
from requests.exceptions import SSLError
import json

MY_KEY = '78bf3faa-4a1a-405c-bf13-d79d90a491da'


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

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': MY_KEY,
}

session = Session()
session.headers.update(headers)