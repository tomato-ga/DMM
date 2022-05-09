import os
import json
from re import search
from socket import if_nameindex
from unicodedata import name
import requests
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

    # floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

    #pprint.pprint(Box.from_json(floor.text))
    # json_box = Box.from_json(floor.text)
    # print(json_box)


    @property
    def search_keyword(self):

        while True:
            search_keyword_response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits={self.hits_count}&sort=rank&keyword={self.keyword}&offset={self.offset_count}&output=json')
            search_json_box = Box.from_json(search_keyword_response.text)
            items = search_json_box.result['items']

            for item in items:
                try:
                    af_url = item.affiliateURL
                    title = item.title
                    video_info = item.sampleMovieURL
                    del video_info.pc_flag, video_info.sp_flag

                    size_array = []
                    video_array = []
                    for size, v_url in video_info.items():

                        max_size_info = size.split('_')
                        split_size = int(max_size_info[1])
                        size_array.append(split_size)
                        video_array.append(v_url)

                    max_size = size_array.index(max(size_array))

                    if str(size_array[max_size]) in v_url:

                        if video_info:
                            yield dict(
                                title=title,
                                aff_url=af_url,
                                video_url=v_url
                        )

                except Exception as ex:
                    print(ex)

                self.offset_count = self.hits_count + self.offset_count

                if len(items) == 0:
                    break

            with open('fanza_genre.json', 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)



if __name__ == '__main__':

    g = Genre_dmm()
    g.APIID = 'b7fkZaG3pW6ZZHpGBbLz'
    g.AFFILIATEID = 'kamipanmen-990'
    g.keyword= 'メンズエステ' # 不要→ keyword.encode('utf-8')
    g.offset_count = 1
    g.hits_count = 20

    for i, video_info in enumerate(g.search_keyword):
        print(i, video_info)