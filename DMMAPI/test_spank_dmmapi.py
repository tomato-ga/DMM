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

floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

# response = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%e3%81%8d&floor_id=25&hits=40&offset=10&output=json')

floor_text = floor.text
floor_data = json.loads(floor_text)
floor_item = floor_data['result']

pprint.pprint(floor_item)


# genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%E3%81%99&floor_id=43&hits=500&offset=1&output=json')

# genre_text = genre.text
# genre_data = json.loads(genre_text)
# genre_item = genre_data['result']


#TODO ジャンルはJSONで保存しておくのがよさそう

all_genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&floor_id=43&hits=500&offset=1&output=json')
all_genre_text = all_genre.text
all_genre_data = json.loads(all_genre_text)
all_genre_item = all_genre_data['result']

for items in all_genre_item['genre']:
    for item in items.values():
        if 'スパンキング' in item:
            spank_url = items['list_url']

spank = requests.get(spank_url)
print(spank)
