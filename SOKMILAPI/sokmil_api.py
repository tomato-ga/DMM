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


        url = search_json_box.result['items'][0]['sampleMovieURL']['url']
        print(url)
        return url


class Down:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)

    def down(self, url):

        self.driver.get(url)
        self.wait.until(EC.presence_of_all_elements_located)
        time.sleep(0.5)
        source = self.driver.page_source
        print(source)

        url_search = re.findall("r'(https:)\\'", source) # (^https://)(\w.*)(.mp4$)
        print(url_search)



s = Sokmil()
s.APIKEY = 'f5fa0b38192389bb264ad32bdb80c802'
s.AFFILIATEID = 24353
s.hits_count = 20
s.offset_count = 1
s.keyword = '奈月セナ'

video_url = s.search_items()

# video_url = 'https://www.sokmil.com/idol/_item/item297385.htm'

d = Down()
d.down(video_url)
