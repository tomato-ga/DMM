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
        self.driver = webdriver.Chrome('/Users/ore/Documents/py_binary/chromedriver', options=self.options)
        # self.driver = webdriver.Chrome(options=self.options)  #options=self.options 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe'
        #self.driver.implicitly_wait(10)

        self.wait = WebDriverWait(driver=self.driver, timeout=30)

    def down(self, index, video_info: dict):
        print(video_info)
        try:
            self.driver.get(video_info['video_url'])
            self.wait.until(EC.presence_of_all_elements_located)
            time.sleep(0.4)
            iframe = self.driver.find_element(by=By.TAG_NAME, value='iframe')
            self.driver.switch_to.frame(iframe)
            elem = self.driver.find_element(by=By.XPATH, value="//main[contains(@id, 'dmmvideo-player')]/video").get_attribute('src')
            print(elem)

            video_response = requests.get(elem)
            time.sleep(15)
            file_name = f'menes_{index}.mp4'
            time.sleep(0.4)
            with open(f'/Volumes/Xeon8TB/don/files/menes_fanza_video/{file_name}', 'wb') as save_v:
                save_v.write(video_response.content)

        except Exception as ex:
            print(ex)
            pass

        return file_name


load_json = json.load(open('/Users/ore/Documents/GitHub/DMM/DMMAPI/fanza_genre.json'))
print(len(load_json['title']))

save_json = {}
save_json['title'] = []

vv = video()
for i, video_info in enumerate(load_json['title']):
    print(i, video_info)
    file_name = vv.down(i, video_info)
    video_info['file_name'] = file_name
    save_json['title'].append(video_info)
    time.sleep(0.4)

with open('/Users/ore/Documents/GitHub/DMM/DMMAPI/fanza_menes_videofile.json', 'w+', encoding='utf-8') as f:
    json.dump(save_json, f, indent=4, ensure_ascii=False)