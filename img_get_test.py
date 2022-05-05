import os
import json
import requests

json_path = open('./overf_all_photos.json')
load = json.load(json_path)
l = load['photo']

for i in l:
    print(i['img'])
    im = requests.get(i['img'])
    os.makedirs(r'/mnt/hdd/don/files/mizugazo/overf/', mode=0o777, exist_ok=True)

    with open(r'/mnt/hdd/don/files/mizugazo/overf/', 'wb') as image:
        image.write(im.content)