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
json_path = '/home/don/py/DMM/wpapi_download/new_mizugazo_all_photos.json'

old_json = json.load(open('/home/don/py/DMM/wpapi_download/old_mizugazo_all_photos.json', 'r'))
old_df = pd.DataFrame(old_json['photo'])
old_imgs = old_df['imgs'].tolist()
get_count = 0

today = datetime.datetime.now()

logger = getMyLogger(str(today))
logger.info(f"Goスタート")

try:
    while True:
        json_url = f'https://mizugazo.com/wp-json/wp/v2/media?per_page={count}&offset={response_offset}'
        res = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
        load_jsons = json.loads(res.text)
        response_offset += 100

        for load_json in load_jsons:
            if load_json['source_url'] not in old_imgs:
                print('image urlがJSONにありません')
                if not load_json:
                    break
                elif load_json:
                    if ' ' in load_json['alt_text']:
                        split = load_json['alt_text']
                        split_tag = split.split()
                        if len(split_tag) == 2:
                            media_info = {
                                'tag': f'{split_tag[0]},{split_tag[1]}',
                                'imgs': load_json['source_url']
                            }
                        elif len(split_tag) == 3:
                            media_info = {
                                'tag': f'{split_tag[0]},{split_tag[1]},{split_tag[2]}',
                                'imgs': load_json['source_url']
                            }
                    else:
                        media_info = {
                            'tag': load_json['alt_text'],
                            'imgs': load_json['source_url']
                        }
                    time.sleep(0.2)
                    print(media_info)
                    all_photo['photo'].append(media_info)
                    old_json['photo'].append(media_info)
                    get_count += 1
                    print(f'取得件数は{get_count}件です')


            elif load_json['source_url'] in old_imgs:
                print('image urlがJSONに入ってます')
                print('取得完了')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(all_photo, f, indent=4, ensure_ascii=False)
                with open('/home/don/py/DMM/wpapi_download/old_mizugazo_all_photos.json', 'w', encoding='utf-8') as f:
                    json.dump(old_json, f, indent=4, ensure_ascii=False)
                break

            elif res.status_code != 200:
                print('取得完了')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(all_photo, f, indent=4, ensure_ascii=False)
                with open('/home/don/py/DMM/wpapi_download/old_mizugazo_all_photos.json', 'w', encoding='utf-8') as f:
                    json.dump(old_json, f, indent=4, ensure_ascii=False)
                break

        if load_json['source_url'] in old_imgs:
            break
        elif res.status_code != 200:
            break


    mizugazo_img_get.image_get()

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