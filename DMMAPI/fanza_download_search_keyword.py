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

    def down(self, index, video_info: dict):
        print(video_info)
        try:
            self.driver.get(video_info['video_url'])
            self.wait.until(EC.presence_of_all_elements_located)
            time.sleep(0.5)
            iframe = self.driver.find_element(by=By.TAG_NAME, value='iframe')
            self.driver.switch_to.frame(iframe)
            elem = self.driver.find_element(by=By.XPATH, value="//main[contains(@id, 'dmmvideo-player')]/video").get_attribute('src')
            print(elem)

            video_response = requests.get(elem)
            time.sleep(0.3)
            file_name = f'irama_{index}.mp4'
            time.sleep(0.2)
            with open(f'/mnt/hdd/don/files/fanza/hazukasi/{file_name}', 'wb') as save_v:
                save_v.write(video_response.content)

            if file_name:
                return file_name
            else:
                return None

        except Exception as ex:
            print(ex)
            pass



load_json = json.load(open('/home/don/py/DMM/DMMAPI/fanza_genreイラマチオ.json'))
print(len(load_json['title']))

save_json = {}
save_json['title'] = []

vv = video()
for i, video_info in enumerate(load_json['title']):
    print(i, video_info)
    try:
        file_name = vv.down(i, video_info)
        if file_name:
            video_info['file_name'] = file_name
            save_json['title'].append(video_info)
            time.sleep(0.2)
    except Exception as ex:
        print(ex)
        pass

with open('/home/don/py/DMM/DMMAPI/fanza_genreイラマチオ_videofile.json', 'w+', encoding='utf-8') as f:
    json.dump(save_json, f, indent=4, ensure_ascii=False)