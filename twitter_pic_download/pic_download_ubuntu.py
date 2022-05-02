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
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        self.img_urls = []


    def chrome_quit(self):
        self.driver.quit()


    def image_url_parse(self, url):

        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_all_elements_located)
            self.driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.END)

            source = self.driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            title = soup.find('h2', {'class': 'entry-title'}).text
            blocks = soup.find('div', {'class': 'entry-content'})
            img_url = blocks.find_all('img')
            os.makedirs(f'/mnt/hdd/don/files/twitphotos/{title}', mode=0o777 , exist_ok=True)

            for img in img_url:
                self.img_urls.append(img['src'])
            print(self.img_urls)

            for img_url in self.img_urls:
                image_get = requests.get(img_url)
                time.sleep(0.3)
                file_name = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', img_url) # TODO ([a-zA-z0-9_-]*)(.[a-z]{3,4}$) ([a-zA-z0-9_-]*)(.jpg)
                file_name = file_name[0][0]
                file_name = file_name.replace('/', '')
                file_ex =  '' # TODO 正規表現で拡張子取って、file_exにいれるところから
                with open(f'/mnt/hdd/don/files/twitphotos/{title}/{str(file_name)}{file_ex}', 'wb') as image: #Win f'E:\\twit_photos\\{title}\\{str(file_name)}.jpg', 'wb' # Ubuntu f'/mnt/hdd/don/files/twitphotos/{title}/{str(file_name)}.jpg', 'wb'
                    image.write(image_get.content)
                    time.sleep(0.3)


        except Exception as ex:
            print('[article_url_parse]', ex)
            pass


t = Image()
urls: list = pd.read_csv('url.csv')
urls = urls.values
for url in urls:
    t.image_url_parse(url[0])

t.chrome_quit()
