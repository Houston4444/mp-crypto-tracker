from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pathlib import Path

base_url = 'https://pro-api.coinmarketcap.com/v2/'
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/listings/latest'

parameters = {
  # 'id':'1',
  # 'start': '1',
  # 'id': 9840,
  # 'limit':'5000',
  # 'id': '9840',
  # 'convert':'EUR'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '78bf3faa-4a1a-405c-bf13-d79d90a491da',
}

session = Session()
session.headers.update(headers)



print('eokez')

pathi = 'https://pro-api.coinmarketcap.com/v1/'

# rourou = pathi  + 'cryptocurrency/' + 'quotes/latest'
rourou = pathi  + 'cryptocurrency/' + 'map'

# try:
if True:
    print('aa:', str(rourou))
    response = session.get(str(rourou), params=parameters)
    # print(response.text)
    data = json.loads(response.text)
    # print('oulalla', len(data['data']))
    with open('api_map.json', 'w') as f:
        json.dump(data, f, indent=4)
# except:
else:
    print('pkpuipoo')

# for path in ('cryptocurrency', 'exchange'):
#     url = f'https://pro-api.coinmarketcap.com/v1/{path}/listings/latest'

#     try:
#         response = session.get(url, params=parameters)
#         data = json.loads(response.text)
#         # print(data)
        
#         with open(f'api_out/{path}.json', 'w') as f: 
#             json.dump(data, f, indent=4)
            
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)
#     except:
#         print('oeppepep')