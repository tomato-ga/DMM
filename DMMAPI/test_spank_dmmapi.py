
import os
# from dmm_api import DMMApiClient
import pprint
import json
import re

APIID = os.environ.get('DMM_API_ID', 'b7fkZaG3pW6ZZHpGBbLz')
AFFILIATEID = os.environ.get('DMM_AFFILIATE_ID', 'kamipanmen-990')

import requests

# response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={API_ID}&affiliate_id={AFFILIATE_ID}&site=FANZA&service=digital&floor=videoa&hits=10&sort=date&keyword=%e4%b8%8a%e5%8e%9f%e4%ba%9c%e8%a1%a3&output=json')

# floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

# # response = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%e3%81%8d&floor_id=25&hits=40&offset=10&output=json')

# floor_text = floor.text
# floor_data = json.loads(floor_text)
# floor_item = floor_data['result']

# pprint.pprint(floor_item)


# genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%E3%81%99&floor_id=43&hits=500&offset=1&output=json')

# genre_text = genre.text
# genre_data = json.loads(genre_text)
# genre_item = genre_data['result']


# initial=%E3%81%99& スパンキング

"""オールジャンル取得"""
# all_genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&floor_id=43&hits=500&offset=1&output=json')
# all_genre_text = all_genre.text
# all_genre_data = json.loads(all_genre_text)
# all_genre_item = all_genre_data['result']

# with open('genre.json', 'w', encoding='utf-8') as f:
#     json.dump(all_genre_item, f, indent=4, ensure_ascii=False)

def jsonload():
    with open('genre.json', 'r', encoding='utf-8') as r:
        genre = json.load(r)
        for items in genre['genre']:
            if 'スパンキング' in items['name']:
                page_url = items['list_url']
                print(page_url)
    return page_url


"""ジャンルに特化した最新の動画を集める"""


def genre_search():
    genre_url = f'https://api.dmm.com/affiliate/v3/ItemList?api_id={APIID}&affiliate_id={AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits=10&sort=date&article=genre&article_id=6940&output=json'
    response = requests.get(genre_url)
    print()
    genre_text = response.text
    genre_data = json.loads(genre_text)
    genre_item = genre_data['result']['items']
    print(genre_item)

    for items in genre_item:
        af_url = items['affiliateURL']
        title = items['title']
        videos_info = items['sampleMovieURL']
        del videos_info['pc_flag'], videos_info['sp_flag']

        size_array = []
        video_array = []
        for size, v_url in videos_info.items():

            max_size_info = size.split('_')
            split_size = int(max_size_info[1])
            size_array.append(split_size)
            video_array.append(v_url)

        max_size = size_array.index(max(size_array))
        if str(size_array[max_size]) in v_url:
            print(size,v_url)

            yield dict(
                title=title,
                aff_url=af_url,
                video_url=v_url
            )

genre_search()


# TODO あとは動画をダウンロードしてDBに保存していくだけ
