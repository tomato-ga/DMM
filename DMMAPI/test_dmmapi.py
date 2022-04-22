import os
from dmm_api import DMMApiClient
import pprint
import json


APIID = os.environ.get('DMM_API_ID', 'b7fkZaG3pW6ZZHpGBbLz')
AFFILIATEID = os.environ.get('DMM_AFFILIATE_ID', 'kamipanmen-990')


# client = DMMApiClient(API_ID, AFFILIATE_ID)
# res = client.get_floor()
# # pprint.pprint(res.json())


# res2 = client.get_item_list(site="FANZA")
# text = res2.text
# data = json.loads(text)

# item = data['result']['items']


# pprint.pprint(data)


import requests

# response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={API_ID}&affiliate_id={AFFILIATE_ID}&site=FANZA&service=digital&floor=videoa&hits=10&sort=date&keyword=%e4%b8%8a%e5%8e%9f%e4%ba%9c%e8%a1%a3&output=json')

floor =  f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json'

response = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%e3%81%8d&floor_id=25&hits=40&offset=10&output=json')

text = floor.text
data = json.loads(text)
item = data['result']

pprint.pprint(item)
