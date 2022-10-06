import os
import random
import requests
import json
import time
import pandas as pd
import datetime

import mizugazo_img_get
from record_log import getMyLogger

count = 100
response_offset = 0
media_offset = 0
all_photo = {}
all_photo['photo'] = []
# json_path = '/home/don/py/DMM/wpapi_download/new_mizugazo_all_posts.json'

# old_json = json.load(open('/home/don/py/DMM/wpapi_download/old_mizugazo_all_posts.json', 'r'))
# old_df = pd.DataFrame(old_json['photo'])
# old_imgs = old_df['imgs'].tolist()
# get_count = 0

today = datetime.datetime.now()

logger = getMyLogger(str(today))
logger.info(f"Goスタート")

try:
    while True:
        json_url = f'https://mizugazo.com/wp-json/wp/v2/posts?per_page={count}&offset={response_offset}'
        res = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
        load_jsons = json.loads(res.text)
        response_offset += 100


except Exception as e:
        logger.exception(e)
        pass

"""
2022/05/14 23:38
更新分だけJSON保存するようにする
old_json
if load_json['source_url'] not in old_imgs:


2022/05/25 15:29
→動作確認中→whileの外だとJSON保存できてない
→breakする前にJSON書き込むように変更


2022/06/04 15:46
import mizugazo_img_get追加

"""