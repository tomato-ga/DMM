import os
import random
import requests
import json
import time


name = 'idle-girl'
count = 100
response_offset = 0
media_offset = 0
all_photo = {}
all_photo['photo'] = []
json_path = f'/home/don/py/DMM/wpapi_download/{name}_all_photos.json'

medias_param = {
    'per_page': count,
    'offset': media_offset
    }


while True:
    json_url = f'https://idle-girl.com/wp-json/wp/v2/posts?per_page={count}&offset={response_offset}'
    res = requests.get(json_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
    load_jsons = json.loads(res.text)
    response_offset += 100

    for load_json in load_jsons:
        if not load_json:
            break
        elif load_json:
            if load_json['_links']['wp:attachment']:
                title: str = load_json['title']['rendered']
                wp_attachment_url: str = load_json['_links']['wp:attachment'][0]['href']
                medias_get: json = requests.get(wp_attachment_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}, params=medias_param)

                match medias_get.status_code:
                    case 200:
                        print(200)
                        load_medias: list = json.loads(medias_get.text)
                        for load_media in load_medias:
                            media_info = {
                                'tag': title,
                                'img': load_media['source_url']
                                }
                            all_photo['photo'].append(media_info)
                            with open(json_path, 'w', encoding='utf-8') as f:
                                json.dump(all_photo, f , indent=4, ensure_ascii=False)
                                time.sleep(0.2)
                                print(media_info)
                    case _:
                        print(200, 'じゃない')




            elif load_json['_links']['wp:attachment'] is None:
                print('passします')
                pass

        else:
            pass

    if res.status_code != 200:
        break

