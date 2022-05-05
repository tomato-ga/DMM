import os
import json
import requests
import re

json_path = open('./overf_all_photos.json')
load = json.load(json_path)
l = load['photo']

try:
    for i in l:
        print(i['img'])
        im = requests.get(i['img'])
        name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', im.url)
        os.makedirs('/mnt/hdd/don/files/mizugazo/overf/', mode=0o777, exist_ok=True)

        with open(f'/mnt/hdd/don/files/mizugazo/overf/{name_search[0][0]}{name_search[0][1]}', 'wb') as image:
            image.write(im.content)
except Exception as ex:
    print(ex)