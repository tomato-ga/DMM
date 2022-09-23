import os
import json
import re
import requests
import time
import pymongo
from box import Box
from dataclasses import dataclass
from datetime import datetime, date, timedelta

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
    sort: str = ""
    gte_date: str = ""
    index_today: str = ""

    def search_items(self):
        search_response = {}
        search_response['title'] = []

        api_url = 'https://sokmil-ad.com/api/v1/Item'
        url_params = {
            'api_key': self.APIKEY,
            'affiliate_id': self.AFFILIATEID,
            'category': 'idol',
            'keyword': self.keyword,
            "sort": self.sort,
            "gte_date": self.gte_date,
            'output': 'json',
            }

        search_keyword_response = requests.get(api_url, params=url_params)
        time.sleep(0.2)
        search_json_box = Box.from_json(search_keyword_response.text)
        print(search_json_box)



        for i, x in enumerate(search_json_box.result['items']):

            yield dict(
                title = x['title'],
                actor = x.iteminfo.actor[0]['name'],
                video_embed_url = x['sampleMovieURL']['url'],
                aff_url =  x['affiliateURL'],
                dates = x['date'],
                price = x.prices['price'],
                index=self.index_today + "_" + str(i))


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

    def down(self, video_info: dict):

        video_embed_url = video_info['video_embed_url']
        index = video_info['index']

        self.driver.get(video_embed_url)
        time.sleep(0.2)
        self.wait.until(EC.presence_of_all_elements_located)
        self.driver.save_screenshot('./1.png')
        source = self.driver.page_source

        search = re.findall(r'([https:\\\])(\w*\.\w*.\w*\\/\w*\\.?\?)(a=)([\w_-]*&h=\w*&\w=\w*.mp4)', source) # 毎回ファイル名がランダムだった
        file_name = f'{index}.mp4'

        search_url_modify = search[0].replace('\\', '')
        video_response = requests.get(search_url_modify)
        # os.makedirs(fr'/mnt/hdd/don/files/sok/{s.keyword}/', mode=0o777, exist_ok=True)
        with open(fr'/mnt/hdd/don/files/sok/new/{file_name}', 'wb') as save_video:
            save_video.write(video_response.content)
        print(video_response)

        return file_name


s = Sokmil()
d = Down()
s.APIKEY = 'f5fa0b38192389bb264ad32bdb80c802'
s.AFFILIATEID = 24353
s.hits_count = 100
s.offset_count = 1
s.keyword = ''
s.sort = "date"


today = datetime.now().replace(microsecond=0)
today = (today - timedelta(days=7)).isoformat()
s.gte_date = today

index_today = datetime.now().replace(microsecond=0).strftime("%Y%m%d")
s.index_today = index_today



db_url = 'mongodb://pyton:radioipad1215@192.168.0.25:27017'
client = pymongo.MongoClient(db_url)
db = client.twitter
collection = db.sokmil

for video_info in s.search_items():
    print(video_info)
    file_name = d.down(video_info)
    video_info['file_name'] = file_name
    collection.insert_one(video_info)


