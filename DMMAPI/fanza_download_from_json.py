from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
import requests
import json
import time
import re
import os
from concurrent.futures import ThreadPoolExecutor


class video:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)

    def down(self, index, video_info: dict, file_name: str):
        print(video_info)
        try:
            self.driver.get(video_info['video_url'])
            self.wait.until(EC.presence_of_all_elements_located)
            time.sleep(0.5)
            iframe = self.driver.find_element(by=By.TAG_NAME, value='iframe')
            self.driver.switch_to.frame(iframe)
            elem = self.driver.find_element(by=By.XPATH, value="//main[contains(@id, 'dmmvideo-player')]/video").get_attribute('src')
            # TODO elemから動画拡張子をreで取得し、サイズの大きい拡張子へ変更させてレスポンス確認


            # サイズ変更
            id_only_url = re.sub('(_[a-z]*)(_[a-z]+)(.mp4)', '', elem)
            add_video = '_mhb_w'
            new_urls = id_only_url + add_video + '.mp4'
            video_response = requests.get(new_urls)
            time.sleep(0.3)

            if video_response.status_code == 200:
                dir_name = file_name
                file_name = f'{index}_{file_name}.mp4'
                time.sleep(0.2)
                os.makedirs(fr'/mnt/hdd/don/files/fanza/{dir_name}', mode=0o777, exist_ok=True)
                with open(f'/mnt/hdd/don/files/fanza/{dir_name}/{file_name}', 'wb') as save_v:
                    save_v.write(video_response.content)

                if file_name:
                    video_info['file_name'] = file_name
                    return video_info
                else:
                    return None


            elif video_response.status_code != 200:
                pass

        except Exception as ex:
            print(ex)
            pass


"""
流れ
①fanzaから取ってきたvideo_url, aff_urlのJSONを読み込む
②file_nameが入ったJSONを書き出すために、JSONファイル名にジャンルを含める

>ダウンロード後
③movie_5secounds_cutでカット実施
④カット後、videofile.jsonのfile_nameに_cutを付与

"""
load_json = json.load(open('/home/don/py/DMM/DMMAPI/fanza_genre_fanza_genre_actress_2000gen_videourl.json'))
print(len(load_json['title']))

save_json = {}
save_json['title'] = []
file_and_json_name = '2000'

vv = video()
for i, video_info in enumerate(load_json['title']):
    print(i, video_info)
    try:
        new_video_info = vv.down(index=i, video_info=video_info, file_name=file_and_json_name)
        if new_video_info:
            # TODO JSONから取り出したビデオ情報にファイル名を入れている メソッド内で全部実行して整合性をとったほうがよさそう
            save_json['title'].append(new_video_info)
            time.sleep(0.2)
    except Exception as ex:
        print(ex)
        pass

with open(f'/home/don/py/DMM/DMMAPI/fanza_genre_{file_and_json_name}_videofile.json', 'w+', encoding='utf-8') as f:
    json.dump(save_json, f, indent=4, ensure_ascii=False)


"""
【課題】
ビットレート最大のファイルをダウンロードするようにする
一番大きいサイズの拡張子でダウンロードする処理を追加
上のサイズ拡張子から総当たりして、レスポンスがあったURLでダウンロードさせる

_sm_s.mp4
3	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_sm_w.mp4
4	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_dmb_s.mp4
5	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_dmb_w.mp4
6	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_mhb_s.mp4
7	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_mhb_w.mp4

↓vr
8	https://cc3001.dmm.co.jp/vrsample/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]vrlite.mp4

# TODO ファイル名とURL先が同じか確認する


【履歴】
・ビデオ解像度最高のファイルしかダウンロードしないように変更

"""