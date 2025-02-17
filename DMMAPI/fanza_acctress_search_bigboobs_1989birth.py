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
    hits_count = 0
    offset_count: int = 0
    actress_hits_count = 0
    actress_offset_count = 0
    gte_bust = 0
    lte_bust = 0
    gte_waist = 0
    lte_waist = 0
    gte_hip = 0
    lte_hip = 0
    gte_height = 0
    lte_height = 0
    gte_date = ''
    gte_birth = ''


    @property
    def search_keyword(self):
        """
        ジャンル検索URL
        https://api.dmm.com/affiliate/v3/ItemList?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits={self.hits_count}&sort=rank&keyword={self.keyword}&offset={self.offset_count}&output=json

        search_json_box.result['items'] ← ジャンルの場合のJSON

        女優検索URL
        峰不二子スリーサイズ B:99.9cm W:55.5cm H:88.8cm Height: 167cm ←誰もいなかった
        https://api.dmm.com/affiliate/v3/ActressSearch?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&gte_bust={self.gte_bust}&lte_bust={self.lte_bust}&gte_waist={self.gte_waist}&lte_waist={self.lte_waist}&gte_hip={self.gte_hip}&lte_hip={self.lte_hip}&gte_height={self.gte_height}&lte_height={self.lte_height}&sort=-bust&hits={self.hits_count}&offset={self.offset_count}&output=json'
        """

        search_response = {}
        search_response['actress'] = []

        while True:

            try:
                search_keyword_response = requests.get(f'https://api.dmm.com/affiliate/v3/ActressSearch?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&gte_bust={self.gte_bust}&lte_bust={self.lte_bust}&gte_waist={self.gte_waist}&lte_waist={self.lte_waist}&gte_hip={self.gte_hip}&lte_hip={self.lte_hip}&gte_height={self.gte_height}&lte_height={self.lte_height}&sort=-bust&hits={self.hits_count}&offset={self.offset_count}&gte_birthday={self.gte_birth}&output=json')
                time.sleep(0.3)
                search_json_box = Box.from_json(search_keyword_response.text)
                result_count = search_json_box.result['result_count']
                items = search_json_box.result['actress']

                print(type(items))
                print(dir(items))
            except Exception as e:
                print(e)
                if result_count == 0:
                    with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_{self.keyword}.json', 'w+', encoding='utf-8') as f:
                        json.dump(search_response, f, indent=4, ensure_ascii=False)
                    break


            for item in items:
                try:
                    print(item)

                    yield dict(
                    actress_name = item.name,
                    actress_id = item.id,
                    birth = item.birthday,
                    cup = item.cup,
                    bust = item.bust,
                    waist = item.waist,
                    hip = item.hip,
                    height = item.height,
                    )

                    search_response["actress"].append(item)
                    print(f'女優は{len(search_response["actress"])}件です')

                except Exception as ex:
                    print(ex)
                    pass


            self.offset_count = self.hits_count + self.offset_count



if __name__ == '__main__':

    g = Genre_dmm()
    g.APIID = 'b7fkZaG3pW6ZZHpGBbLz'
    g.AFFILIATEID = 'kamipanmen-990'
    g.keyword= 'actress_bust_90to99' # 不要→ keyword.encode('utf-8')
    g.offset_count = 1
    g.hits_count = 20
    g.actress_offset_count = 1
    g.actress_hits_count = 100

    g.gte_bust = 90
    g.lte_bust = 99
    g.gte_waist = 50
    g.lte_waist = 64
    g.gte_hip = 80
    g.lte_hip = 95
    g.gte_height = 140
    g.lte_height = 175
    g.gte_date = '2017-04-01T00:00:00'
    g.gte_birth = '1989-01-01'

    save_json = {}
    save_json['title'] = []
    for i, video_info in enumerate(g.search_keyword):
        print(i, video_info)
        # TODO ここでif not in でなかったら追加する形にする
        save_json['title'].append(video_info)
        with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_{g.keyword}.json', 'w+', encoding='utf-8') as f:
            json.dump(save_json, f, indent=4, ensure_ascii=False)