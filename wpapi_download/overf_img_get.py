import os
import json
import requests
import re
import time


json_path = open('./overf_all_photos.json')
load = json.load(json_path)
l = load['photo']

try:
    for i in l:
        print(i['img'])
        title = i['tag']
        img_url = i['img']
        im_get = requests.get(img_url)
        name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', im_get.url)
        time.sleep(0.2)


        match im_get.status_code:
            case 200:
                os.makedirs(f'/mnt/hdd/don/files/overf/{title}', mode=0o777, exist_ok=True)
                with open(f'/mnt/hdd/don/files/overf/{title}/{name_search[0][0]}{name_search[0][1]}', 'wb') as image:
                    image.write(im_get.content)
                    print('保存完了')
            case _:
                pass

except Exception as ex:
    print(ex)