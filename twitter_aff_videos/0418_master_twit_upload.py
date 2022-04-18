from bs4 import BeautifulSoup
import pandas as pd
import time
import pymongo
import random
import pandas as pd
import glob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tweet:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--window-size=800,600')
        self.options.add_argument('--ignore-certificate-errors')
        # self.options.add_argument('--disable-desktop-notifications')
        # self.options.add_argument("--disable-extensions")
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options)  #options=self.options 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe'
        #self.driver.implicitly_wait(10)
        self.wait1 = random.random()
        self.wait2 = random.randint(3,6)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        self.twitter = 'https://twitter.com/login'


    def db_set(self):
        db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
        client = pymongo.MongoClient(db_url)
        db = client.twitter
        collection = db.affvideos

        return collection

    def db_read(self):
        collection = self.db_set()
        curs = collection.find()
        df = pd.DataFrame.from_dict(list(curs)).astype(object)

        return df

    def Uploads(self):
        account = 'tomorrow_genkio'
        password = 'asdflkjh'

        self.driver.get(self.twitter)
        self.wait.until(EC.presence_of_all_elements_located)
        time.sleep(3)

        elem_account = self.driver.find_element(by=By.XPATH, value="//input[contains(@autocapitalize, 'sentences')]")
        elem_account.send_keys(account)
        time.sleep(3)

        self.wait.until(EC.presence_of_all_elements_located)
        next_button = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), '次へ')]")
        next_button.click()
        time.sleep(3)

        self.wait.until(EC.presence_of_all_elements_located)
        elem_pass = self.driver.find_element(by=By.XPATH, value="//input[contains(@autocomplete, 'current-password')]")
        elem_pass.send_keys(password)
        time.sleep(3)

        self.wait.until(EC.presence_of_all_elements_located)
        login = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), 'ログイン')]")
        login.click()
        time.sleep(3)


        df = self.db_read()
        random_video = df.sample()
        upload_video_file_name: str = random_video['video_file'].values[0]
        upload_url: str = random_video['url'].values[0]


        # ファイルパスを入力
        self.wait.until(EC.presence_of_all_elements_located)
        video_path = glob.glob(f'/mnt/hdd/don/files/twitvideo/{upload_video_file_name}')     # Windows ('E:\\twitvideo\\vfNE_p1K-0GNdQfF.mp4')
        self.driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(video_path)
        time.sleep(2)

        # テキスト入力
        self.wait.until(EC.presence_of_all_elements_located)
        text = f'この動画を特定したぞ→ {upload_url}'
        elem_text = self.driver.find_element(by=By.CLASS_NAME, value='notranslate')
        elem_text.click()
        elem_text.send_keys(text)
        time.sleep(1)

        # 投稿
        tweet_button = self.driver.find_element(by=By.XPATH, value='//*[@data-testid="tweetButtonInline"]')
        tweet_button.click()
        time.sleep(40)
        self.wait.until(EC.presence_of_all_elements_located)


i = Tweet()
i.Uploads()
