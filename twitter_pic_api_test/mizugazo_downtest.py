import os
import random
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor
import re


json_f = open('./mizugazo_all_photos.json', 'r')
load = json.load(json_f)
loads = load['photo']

for zz in loads:
    try:
        tag = zz['tag']
        img_url = zz['imgs']
        img_get = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
        time.sleep(0.3)
        print(tag, img_url)

        name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', img_url) # TODO ([a-zA-z0-9_-]*)(.[a-z]{3,4}$) ([a-zA-z0-9_-]*)(.jpg)
        file_name = name_search[0][0]
        file_ex =  name_search[0][1] # TODO 正規表現で拡張子取って、file_exにいれるところから
        print(file_name, file_ex)

        if ',' in tag:
            split_tag = tag.split(',')
            title = split_tag[0]
            os.makedirs(f'/mnt/hdd/don/files/mizugazo/{title}', mode=0o777 , exist_ok=True)
            with open(f'/mnt/hdd/don/files/mizugazo/{title}/{file_name}{file_ex}', 'wb') as image:
                image.write(img_get.content)
                print(f'{file_name}{file_ex}:書き込み完了')
        else:
            title = tag
            os.makedirs(f'/mnt/hdd/don/files/mizugazo/{title}', mode=0o777 , exist_ok=True)
            with open(f'/mnt/hdd/don/files/mizugazo/{title}/{file_name}{file_ex}', 'wb') as image:
                image.write(img_get.content)
                print(f'{file_name}{file_ex}:書き込み完了')

    except Exception as ex:
        print(ex)


