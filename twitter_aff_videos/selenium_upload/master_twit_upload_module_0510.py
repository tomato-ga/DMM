from bs4 import BeautifulSoup
import pandas as pd
import time
import pymongo
import random
import pandas as pd
import glob
import os
import datetime
from record_log import getMyLogger


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome import service as fs

wait_1 = random.random()
wait_2 = random.randint(5,15) # 50, 400
randomwait = round(wait_1 + wait_2, 5)


class Tweet:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--lang=ja-JP')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
        self.driver = webdriver.Chrome(options=self.options) # Mac '/Volumes/SSD_1TB/Down/chromedriver'
        self.driver.set_window_size('1200', '1800')

        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        self.twitter = 'https://twitter.com/i/flow/login'


    def db_set(self):
        db_url = 'mongodb://pyton:radioipad1215@192.168.0.25:27017'
        client = pymongo.MongoClient(db_url)
        db = client.twitter
        collection = db.videos

        return collection

    def db_read(self):
        collection = self.db_set()
        curs = collection.find()
        df = pd.DataFrame.from_dict(list(curs)).astype(object)

        return df

    def Uploads(self, account: str):

        today = datetime.datetime.now()
        logger = getMyLogger(str(today)).getChild(__file__)
        logger.info(f"{account}スタート")

        time.sleep(randomwait) #投稿時間をランダムにする時間

        account = account
        password = 'asdflkjh'

        try:
            self.driver.get(self.twitter)
            time.sleep(150)

            self.driver.save_screenshot('/home/don/py/DMM/twitter_aff_videos/selenium_upload/1.png')

            elem_account = self.driver.find_element(by=By.XPATH, value="//input[contains(@autocapitalize, 'sentences')]")
            elem_account.send_keys(account)
            time.sleep(10)
            self.driver.save_screenshot('2.png')


            self.driver.implicitly_wait(10)
            self.wait.until(EC.presence_of_all_elements_located)
            next_button = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), '次へ')]")
            self.driver.execute_script('arguments[0].click();', next_button)
            time.sleep(6)

            print(self.driver.current_url)
            self.driver.save_screenshot('/home/don/py/DMM/twitter_aff_videos/selenium_upload/2.png')
            self.wait.until(EC.presence_of_all_elements_located)
            elem_pass = self.driver.find_element(by=By.XPATH, value="//input[contains(@name, 'password')]")
            elem_pass.send_keys(password)
            time.sleep(6)

            self.driver.implicitly_wait(20)
            self.wait.until(EC.presence_of_all_elements_located)
            login = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), 'ログイン')]")
            self.driver.execute_script('arguments[0].click();', login)
            time.sleep(6)
            print('ログインしました')
            self.driver.save_screenshot('3.png')


            df = self.db_read()
            random_video = df.sample()
            upload_video_file_name: str = random_video['video_file'].values[0]
            upload_url: str = random_video['url'].values[0]
            print(upload_video_file_name, ':', upload_url)

            if upload_url is not None: # TODO tomorro 1j_mcはupload_urlはあるままでOK DBからaff_urlを呼び出してるだけ

                # ファイルパスを入力
                """Ubuntuの場合、glob.globではなく、os.path.abspathにしたらアップできた!!
                Windowsはglob.glob
                Ubuntuはos.path.abspath
                """
                self.wait.until(EC.presence_of_all_elements_located)
                video_path = os.path.abspath(f'/mnt/hdd/don/files/twitvideo/{upload_video_file_name}')
                self.driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(video_path)
                time.sleep(2)

                # テキスト入力
                self.wait.until(EC.presence_of_all_elements_located)

                ######################################## 2022/05/23 0:02 テキストURL消す
                # text = f'{text}' + ' '+ f'{upload_url}'
                # elem_text = self.driver.find_element(by=By.CLASS_NAME, value='notranslate')
                # self.driver.execute_script('arguments[0].click();', elem_text)
                # elem_text.send_keys(text)
                # time.sleep(1)
                ########################################テキストURL消す########################################

                # 投稿
                tweet_button = self.driver.find_element(by=By.XPATH, value='//*[@data-testid="tweetButtonInline"]')
                self.driver.execute_script('arguments[0].click();', tweet_button)
                #tweet_button.click()
                time.sleep(20) #動画がアップロードされるまでの待機時間
                self.wait.until(EC.presence_of_all_elements_located)

        except Exception as ex:
            print('[Uploads]:', ex)
            logger.exception(ex)
            pass

        logger.info("正常終了しました")

    def Quit(self):
        self.driver.quit()



"""変更履歴
2022/05/10 21:59
sleep 20秒設定

self.driver.get(self.twitter)
time.sleep(20)

リトライテスト
@retry(tries=7, delay=10)

2022/05/11 19:35
click()からexecute_scriptへ変更
解像度を縦1800へ変更

2022/05/23 0:02
テキスト・URL消す

2022/08/02
logger追加

ログインURLを変更
https://twitter.com/login
↓
https://twitter.com/i/flow/login


"""