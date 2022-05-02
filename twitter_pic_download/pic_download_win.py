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
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        chromedriver = 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe' # '/Users/oono/Documents/py_binary/chromedriver'
        chrome_service = fs.Service(executable_path=chromedriver)
        self.driver = webdriver.Chrome(service=chrome_service, options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        ###################Windows########################

    @property
    def chrome_quit(self):
        self.driver.quit()


    def image_url_parse(self, url):

        img_urls = []
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_all_elements_located)
            self.driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.END)

            source = self.driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            title = soup.find('h2', {'class': 'entry-title'}).text
            blocks = soup.find('div', {'class': 'entry-content'})
            img_url = blocks.find_all('img')
            os.makedirs(f'E:\\twit_photos\\{title}', mode=0o777 , exist_ok=True)

            for img in img_url:
                img_urls.append(img['src'])

            print(img_urls)
            print(len(img_urls))
            for img_url in img_urls:
                image_get = requests.get(img_url)
                time.sleep(0.3)
                name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', img_url) # TODO ([a-zA-z0-9_-]*)(.[a-z]{3,4}$) ([a-zA-z0-9_-]*)(.jpg)
                file_name = name_search[0][0]
                file_name = file_name.replace('/', '')
                file_ex =  name_search[0][1] # TODO 正規表現で拡張子取って、file_exにいれるところから
                with open(f'E:\\twit_photos\\{title}\\{str(file_name)}{file_ex}', 'wb') as image: #Win f'E:\\twit_photos\\{title}\\{str(file_name)}.jpg', 'wb' # Ubuntu f'/mnt/hdd/don/files/twitphotos/{title}/{str(file_name)}.jpg', 'wb'
                    image.write(image_get.content)
                    time.sleep(0.3)


        except Exception as ex:
            print('[article_url_parse]', ex)
            pass


t = Image()
urls: list = pd.read_csv('C:\\Users\\PC_User\\Documents\\GitHub\\DMM\\twitter_pic_download\\url.csv')
urls = urls.values
for url in urls:
    t.image_url_parse(url[0])

t.chrome_quit
