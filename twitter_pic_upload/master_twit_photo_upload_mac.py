from bs4 import BeautifulSoup
import pandas as pd
import time
import pymongo
import random
import pandas as pd
import glob
import os
from retry import retry

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

wait_1 = random.random()
wait_2 = random.randint(5,6) # TODO テスト中は短め
randomwait = round(wait_1 + wait_2, 5)


class Tweet:


    def __init__(self):
        self.options = Options()
        self.options.add_argument('--lang=ja-JP')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome('/Volumes/SSD_1TB/Down/chromedriver', options=self.options) # Mac '/Volumes/SSD_1TB/Down/chromedriver'
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        self.twitter = 'https://twitter.com/login'

    def Uploads(self, account: str, password: str, text: str, pic_dir: str):
        """2022/05/10雪平指定になってる"""
        time.sleep(randomwait) #投稿時間をランダムにする時間
        account = account
        password = password

        try:
            self.driver.get(self.twitter)
            # time.sleep(30)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@autocapitalize, 'sentences')]")))
            print(self.driver.current_url)
            self.driver.save_screenshot('1.png')

            elem_account = self.driver.find_element(by=By.XPATH, value="//input[contains(@autocapitalize, 'sentences')]")
            elem_account.send_keys(account)
            time.sleep(10)

            self.wait.until(EC.presence_of_all_elements_located)
            next_button = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), '次へ')]")
            self.driver.execute_script('arguments[0].click();', next_button)
            time.sleep(6)

            print(self.driver.current_url)
            self.driver.save_screenshot('2.png')
            self.wait.until(EC.presence_of_all_elements_located)
            elem_pass = self.driver.find_element(by=By.XPATH, value="//input[contains(@name, 'password')]")
            elem_pass.send_keys(password)
            time.sleep(6)

            self.wait.until(EC.presence_of_all_elements_located)
            login = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), 'ログイン')]")
            self.driver.execute_script('arguments[0].click();', login)
            time.sleep(10)
            print('ログインしました')
            self.driver.save_screenshot('3.png')

            ################ 動画の場合 ################
            # df = self.db_read()
            # random_video = df.sample()
            # upload_video_file_name: str = random_video['video_file'].values[0]
            # upload_url: str = random_video['url'].values[0]
            # print(upload_video_file_name, ':', upload_url)
            ################ 動画の場合 ################

            ################ 画像の場合 ################

            # pic_dir = '/mnt/hdd/don/files/twitphotos_gurasen/' #'E:\\twit_photos_gurasen\\'
            # pic_subdir = os.listdir(pic_dir) # サブディレクトリ一覧
            # random.shuffle(pic_subdir) # サブディレクトリをランダム化
            # photo_lists = os.listdir(pic_dir + pic_subdir[0]) # 画像ファイル一覧
            # random.shuffle(photo_lists) # 画像ファイル一覧をランダム化
            # up_photo = os.path.abspath(pic_dir + pic_subdir[0] + '/' + photo_lists[0])  # Win (pic_dir + pic_subdir[0] + '\\' + photo_lists[0]) # アップするファイルパス取得

            ############################ディレクトリ指定############################

            pic_dir = pic_dir
            photo_lists = os.listdir(pic_dir) # 画像ファイル一覧
            random.shuffle(photo_lists) # 画像ファイル一覧をランダム化
            ext = os.path.splitext(photo_lists[0])
            up_photo = os.path.abspath(pic_dir + photo_lists[0])
            print(up_photo)

            ############################ディレクトリ指定############################
            match ext[1]:

                case '.jpg' | '.jpeg' | '.png':
                    print('jpgかpngです')

                    # ファイルパスを入力
                    self.wait.until(EC.presence_of_all_elements_located)
                    time.sleep(3)
                    upload_path = os.path.abspath(up_photo)     # Windows (f'X:\\don\\files\\twitvideo\\{upload_video_file_name}') #Ubuntu (f'/mnt/hdd/don/files/twitvideo/{upload_video_file_name}')
                    self.driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(upload_path)
                    time.sleep(2)
                    #assert len(text) < 140, '140文字以下じゃない'


                    # テキスト入力
                    self.wait.until(EC.presence_of_all_elements_located)
                    time.sleep(1)
                    text = text # f'{text}' テキストいれるとき
                    elem_text = self.driver.find_element(by=By.CLASS_NAME, value='notranslate')
                    self.driver.execute_script('arguments[0].click();', elem_text)
                    elem_text.send_keys(text)
                    time.sleep(1)

                    # 投稿
                    tweet_button = self.driver.find_element(by=By.XPATH, value='//*[@data-testid="tweetButtonInline"]')
                    self.driver.execute_script('arguments[0].click();', tweet_button)
                    #tweet_button.click()
                    time.sleep(20) #画像がアップロードされるまでの待機時間
                    self.wait.until(EC.presence_of_all_elements_located)

                case _:
                    print('jpgとpng以外です')
                    pass

        except Exception as ex:
            print('[Uploads]:', ex)
            pass


    def Quit(self):
        self.driver.quit()



"""変更履歴

2022/05/11 19:35
click()からexecute_scriptへ変更
解像度を縦1800へ変更
"""