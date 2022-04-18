import os
from dmm_api import DMMApiClient
import pprint

API_ID = os.environ.get('DMM_API_ID', 'b7fkZaG3pW6ZZHpGBbLz')
AFFILIATE_ID = os.environ.get('DMM_AFFILIATE_ID', 'kamipanmen-990')

client = DMMApiClient(API_ID, AFFILIATE_ID)
res = client.get_floor()
pprint.pprint(res.json())


import requests

tes = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={API_ID}&affiliate_id={AFFILIATE_ID}&site=FANZA&service=digital&floor=videoa&hits=10&sort=date&keyword=%e4%b8%8a%e5%8e%9f%e4%ba%9c%e8%a1%a3&output=json')
print(tes)

#TODO APIについてUdemy勉強する
