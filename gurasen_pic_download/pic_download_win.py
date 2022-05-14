from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import pandas as pd
import glob
import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import service as fs


class Image:


    def __init__(self):
        """_summary_Chromedriver初期化👉Windows用
        """

        ###################Windows########################
        # self.options = Options()
        # self.options.add_argument('--headless')
        # self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        # chromedriver = 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe' # '/Users/oono/Documents/py_binary/chromedriver'
        # chrome_service = fs.Service(executable_path=chromedriver)
        # self.driver = webdriver.Chrome(service=chrome_service, options=self.options)
        # self.wait = WebDriverWait(driver=self.driver, timeout=30)
        ###################Windows########################

    @property
    def chrome_quit(self):
        self.driver.quit()


    def image_url_parse(self, url, count):

        img_urls = []
        try:
            source = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
            soup = BeautifulSoup(source.text, 'html.parser')

            title = soup.find('h1', {'class': 'article-title'}).text
            blocks = soup.find('div', {'class': 'article-body'})
            img_url = blocks.find_all('img', {'class': 'pict'})
            save_img_urls = [img for img in img_url if 'livedoor.blogimg.jp' in img['src']]
            print(save_img_urls)

            for img in img_url:
                img_urls.append(img['src'])

            print(img_urls)
            print(len(img_urls))

            os.makedirs(f'E:\\twit_photos_gurasen\\{count}', mode=0o777 , exist_ok=True) #  mode=0o777 , exist_ok=True
            for img_url in img_urls:
                image_get = requests.get(img_url)
                if image_get.status_code == 200:
                    time.sleep(0.5)
                    name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', img_url)
                    file_name = name_search[0][0]
                    file_ex =  name_search[0][1]
                    with open(f'E:\\twit_photos_gurasen\\{count}\\{str(file_name)}{file_ex}', 'wb') as image: #Win f'E:\\twit_photos\\{title}\\{str(file_name)}.jpg', 'wb' # Ubuntu f'/mnt/hdd/don/files/twitphotos/{title}/{str(file_name)}.jpg', 'wb'
                        image.write(image_get.content)
                        time.sleep(0.4)


        except Exception as ex:
            print('[image_url_parse]', ex)
            pass


t = Image()
urls: list = pd.read_csv('C:\\Users\\PC_User\\Documents\\GitHub\\DMM\\gurasen_pic_download\\url.csv')
urls = urls['url'].values

count = 1
for url_string in urls:
    df_urls = eval(url_string)
    for url in df_urls:
        t.image_url_parse(url, count)
        count += 1
        time.sleep(10)
