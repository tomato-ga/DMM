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
            source = self.driver.page_source
            print(elem)

            video_response = requests.get(elem)
            time.sleep(0.3)
            file_name = f'{file_name}_{index}.mp4'
            time.sleep(0.2)
            with open(f'/mnt/hdd/don/files/fanza/bust90to99/{file_name}', 'wb') as save_v:
                save_v.write(video_response.content)

            if file_name:
                return file_name
            else:
                return None

        except Exception as ex:
            print(ex)
            pass


"""
流れ
①fanzaから取ってきたvideo_url, aff_urlのJSONを読み込む
②file_nameが入ったJSONを書き出すために、JSONファイル名にジャンルを含める
③ダウンロードフォルダを設定する

"""
load_json = json.load(open('/home/don/py/DMM/DMMAPI/fanza_genre_actress_bust_90to99_videourl.json'))
print(len(load_json['title']))

save_json = {}
save_json['title'] = []
file_json_name = 'bust90to99'

vv = video()
for i, video_info in enumerate(load_json['title']):
    print(i, video_info)
    try:
        file_name = vv.down(i, video_info, file_name=file_json_name)
        if file_name:
            video_info['file_name'] = file_name
            save_json['title'].append(video_info)
            time.sleep(0.2)
            with open(f'/home/don/py/DMM/DMMAPI/fanza_genre_{file_json_name}_videofile.json', 'w+', encoding='utf-8') as f:
                json.dump(save_json, f, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(ex)
        pass


"""
課題
ビットレート最大のファイルをダウンロードするようにする


# TODO 一番大きいサイズの拡張子でダウンロードする
上のサイズ拡張子から総当たりして、レスポンスがあったURLでダウンロードさせる

_sm_s.mp4
3	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_sm_w.mp4
4	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_dmb_s.mp4
5	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_dmb_w.mp4
6	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_mhb_s.mp4
7	https://cc3001.dmm.co.jp/litevideo/freepv/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]_mhb_w.mp4


↓vr
8	https://cc3001.dmm.co.jp/vrsample/[content_id[1]]/[content_id[1:3]]/[content_id]/[content_id]vrlite.mp4


"""