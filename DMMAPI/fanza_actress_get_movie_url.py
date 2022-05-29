import os
import json
from re import search
from socket import if_nameindex
from unicodedata import name
import requests
import time
import pprint
from box import Box
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class Genre_dmm:

    APIID: str = ''
    AFFILIATEID: str = ''
    keyword: str = ''
    offset_count: int = 0
    hits_count = 0
    save_json = {}
    save_json['title'] = []
    # floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

    #pprint.pprint(Box.from_json(floor.text))
    # json_box = Box.from_json(floor.text)
    # print(json_box)

    def search_keyword(self, actress_id):
        search_response = {}
        search_response['title'] = []

        api_url = 'https://api.dmm.com/affiliate/v3/ItemList'
        url_params = {
            'api_id': self.APIID,
            'affiliate_id': self.AFFILIATEID,
            'hits': self.hits_count,
            'offset': self.offset_count,
            'keyword': '',
            'article': 'actress',
            'article_id': actress_id,
            'site': 'FANZA',
            'service': 'digital',
            'floor': 'videoa',
            'sort': 'rank',
            'output': 'json'
        }
        while True:
            search_keyword_response = requests.get(api_url, params=url_params)
            time.sleep(0.3)
            search_json_box = Box.from_json(search_keyword_response.text)
            items = search_json_box.result['items']
            print(type(items))
            print(dir(items))

            for item in items:
                try:
                    average = item.review.average
                    if float(average) >= 4:
                        af_url = item.affiliateURL
                        title = item.title
                        video_info = item.sampleMovieURL
                        del video_info.pc_flag, video_info.sp_flag
                        print(title)

                        if video_info:
                            size_array = []
                            video_array = []
                            for size, v_url in video_info.items():

                                max_size_info = size.split('_')
                                split_size = int(max_size_info[1])
                                size_array.append(split_size)
                                video_array.append(v_url)

                            max_size = size_array.index(max(size_array))
                            search_response['title'].append(item.to_dict())

                            if str(size_array[max_size]) in v_url:
                                if video_info:
                                    self.save_json['title'].append(dict(
                                        title=title,
                                        aff_url=af_url,
                                        video_url=v_url
                                ))

                except Exception as ex:
                    print(ex)
                    pass

            if search_keyword_response.next == None:
                break

        with open(f'/home/don/py/DMM/DMMAPI/fanza_genre_{g.keyword}_videourl.json', 'w+', encoding='utf-8') as f:
            json.dump(self.save_json, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':

    g = Genre_dmm()
    g.APIID = 'b7fkZaG3pW6ZZHpGBbLz'
    g.AFFILIATEID = 'kamipanmen-990'
    g.keyword= 'fanza_genre_actress_2000gen' # 不要→ keyword.encode('utf-8')
    g.offset_count = 1
    g.hits_count = 20


    load_json = json.load(open('/home/don/py/DMM/DMMAPI/fanza_genre_actress_2000gen.json'))
    actress_json = load_json['title']
    for actress in actress_json:
        g.search_keyword(actress['actress_id'])

