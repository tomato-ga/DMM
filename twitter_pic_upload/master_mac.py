import pandas as pd
import time
import pymongo
import random
import pandas as pd
import glob
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

wait_1 = random.random()
wait_2 = random.randint(1,2) # TODO テスト中は短め
randomwait = round(wait_1 + wait_2, 5)


class Tweet:


    def __init__(self):
        self.options = Options()
        #self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # self.driver = webdriver.Chrome(options=self.options)  #options=self.options 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe'
        #self.driver.implicitly_wait(10)

        self.wait = WebDriverWait(driver=self.driver, timeout=30)
        self.twitter = 'https://twitter.com/login'

    def Uploads(self, account: str, text: str):
        time.sleep(randomwait) #投稿時間をランダムにする時間
        account = account
        password = 'asdflkjh'

        try:
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
            elem_pass = self.driver.find_element(by=By.XPATH, value="//input[contains(@name, 'password')]")
            elem_pass.send_keys(password)
            time.sleep(3)

            self.wait.until(EC.presence_of_all_elements_located)
            login = self.driver.find_element(by=By.XPATH, value="//div[@role='button']/div[@dir='auto']//span[contains(text(), 'ログイン')]")
            login.click()
            time.sleep(3)
            print('ログインしました')

            ################ 動画の場合 ################
            # df = self.db_read()
            # random_video = df.sample()
            # upload_video_file_name: str = random_video['video_file'].values[0]
            # upload_url: str = random_video['url'].values[0]
            # print(upload_video_file_name, ':', upload_url)
            ################ 動画の場合 ################

            ################ 画像の場合 ################

            pic_dir = '/Volumes/SSD_1TB/twitphotos_gurasen'  # '/mnt/hdd/don/files/twitphotos_gurasen/' #'E:\\twit_photos_gurasen\\'
            pic_subdir = os.listdir(pic_dir) # サブディレクトリ一覧
            random.shuffle(pic_subdir) # サブディレクトリをランダム化
            photo_lists = os.listdir(pic_dir + pic_subdir[0]) # 画像ファイル一覧
            random.shuffle(photo_lists) # 画像ファイル一覧をランダム化
            up_photo = os.path.abspath(pic_dir + pic_subdir[0] + '/' + photo_lists[0])  # Win (pic_dir + pic_subdir[0] + '\\' + photo_lists[0]) # アップするファイルパス取得

            if up_photo.endswith('.jpg'):
                print('jpgです')

                # ファイルパスを入力
                """Ubuntuの場合、glob.globではなく、os.path.abspathにしたらアップできた!!
                Windowsはglob.glob
                Ubuntuはos.path.abspath
                """
                self.wait.until(EC.presence_of_all_elements_located)
                upload_path = os.path.abspath(up_photo)     # Windows (f'X:\\don\\files\\twitvideo\\{upload_video_file_name}') #Ubuntu (f'/mnt/hdd/don/files/twitvideo/{upload_video_file_name}')
                self.driver.find_element(by=By.XPATH, value="//input[@type='file']").send_keys(upload_path)
                time.sleep(2)
                assert upload_path == True
                print(upload_path)

                # テキスト入力
                self.wait.until(EC.presence_of_all_elements_located)
                text = text # f'{text}' テキストいれるとき
                elem_text = self.driver.find_element(by=By.CLASS_NAME, value='notranslate')
                elem_text.click()
                elem_text.send_keys(text)
                time.sleep(1)

                # 投稿
                tweet_button = self.driver.find_element(by=By.XPATH, value='//*[@data-testid="tweetButtonInline"]')
                tweet_button.click()
                time.sleep(20) #画像がアップロードされるまでの待機時間
                self.wait.until(EC.presence_of_all_elements_located)

            elif up_photo.endswith('.png'):
                print('pngです')
                pass
            else:
                print('jpgとpng以外です')
                pass

        except Exception as ex:
            print('[Uploads]:', ex)
            pass


    def Quit(self):
        self.driver.quit()



