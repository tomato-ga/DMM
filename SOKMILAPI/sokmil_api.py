import os
import json
import re
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
class Sokmil:
    APIKEY: str = ''
    AFFILIATEID: int = 0
    keyword: str = ''
    hits_count = 0
    offset_count: int = 0
    keyword: str = ''

    def search_items(self):
        search_response = {}
        search_response['title'] = []

        api_url = 'https://sokmil-ad.com/api/v1/Item'
        url_params = {
            'api_key': self.APIKEY,
            'affiliate_id': self.AFFILIATEID,
            'category': 'idol',
            'keyword': self.keyword,
            'output': 'json',

            }

        search_keyword_response = requests.get(api_url, params=url_params)
        time.sleep(0.2)
        search_json_box = Box.from_json(search_keyword_response.text)
        print(search_json_box)

        for i, x in enumerate(search_json_box.result['items']):
            url = x['sampleMovieURL']['url']
            yield i, url


class Down(Sokmil):

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--lang=ja-JP')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)

    def down(self, index, url):

        self.driver.get(url)
        time.sleep(0.2)
        self.wait.until(EC.presence_of_all_elements_located)
        self.driver.save_screenshot('./1.png')
        source = self.driver.page_source

        search = re.findall(r'([https:\\\])(\w*\.\w*.\w*\\/\w*\\.?\?)(a=)([\w_-]*&h=\w*&\w=\w*.mp4)', source) # 毎回ファイル名がランダムだった

        search_url_modify = search[0].replace('\\', '')
        video_response = requests.get(search_url_modify)
        with open(f'/mnt/hdd2/{index}.mp4', 'wb') as save_video:   # Ubuntu f'/mnt/hdd/don/files/twitvideo/ //  Win f'E:\\twitvideo\\{str(v_url_file_name)}.mp4',
            save_video.write(video_response.content)
        print(video_response)



s = Sokmil()
d = Down()
s.APIKEY = 'f5fa0b38192389bb264ad32bdb80c802'
s.AFFILIATEID = 24353
s.hits_count = 20
s.offset_count = 1
s.keyword = '浅川梨奈'

for i, video_url in s.search_items():
    d.down(i, video_url)
