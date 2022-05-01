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

        ###################Windows########################
        # self.options = Options()
        # self.options.add_argument('--headless')
        # self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        # chromedriver = 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe' # '/Users/oono/Documents/py_binary/chromedriver'
        # chrome_service = fs.Service(executable_path=chromedriver)
        # self.driver = webdriver.Chrome(service=chrome_service, options=self.options)
        ###################Windows########################
        self.wait = WebDriverWait(driver=self.driver, timeout=30)


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
            os.mkdir(f'/mnt/hdd/don/files/twitphotos/{title}', mode=777)

            for img in img_url:
                img_urls.append(img['src'])
            print(img_urls)

            for img_url in img_urls:
                image_get = requests.get(img_url)
                time.sleep(0.2)
                file_name = re.findall('([a-zA-z0-9_-]*)(.jpg)', img_url)
                file_name = file_name[0][0]
                file_name = file_name.replace('/', '')
                with open(f'/mnt/hdd/don/files/twitphotos/{title}/{str(file_name)}.jpg', 'wb') as image: #Win f'E:\\twit_photos\\{title}\\{str(file_name)}.jpg', 'wb'
                    image.write(image_get.content)
                    time.sleep(0.2)


        except Exception as ex:
            print('[article_url_parse]', ex)
            pass

        return self.img_urls

t = Image()

urls: list = pd.read_csv('url.csv')
urls = urls.values
for url in urls:
    t.image_url_parse(url[0])
