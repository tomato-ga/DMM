import os
import json
import requests
import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


APIID = os.environ.get('DMM_API_ID', 'b7fkZaG3pW6ZZHpGBbLz')
AFFILIATEID = os.environ.get('DMM_AFFILIATE_ID', 'kamipanmen-990')


# response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={API_ID}&affiliate_id={AFFILIATE_ID}&site=FANZA&service=digital&floor=videoa&hits=10&sort=date&keyword=%e4%b8%8a%e5%8e%9f%e4%ba%9c%e8%a1%a3&output=json')

floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

response = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&initial=%e3%81%8d&floor_id=25&hits=40&offset=10&output=json')

floor_text = floor.text
floor_data = json.loads(floor_text)
floor_item = floor_data['result']

pprint.pprint(floor_item)

#コミック id 82

# genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&floor_id=82&hits=500&offset=1&output=json')

# genre_text = genre.text
# genre_data = json.loads(genre_text)
# genre_item = genre_data['result']

# pprint.pprint(genre_item)

"""コミック"""
#コミック辱め ID 27

hits_count = 20
offset_count = 1
genre_id = 82

genre_url = f'https://api.dmm.com/affiliate/v3/ItemList?api_id={APIID}&affiliate_id={AFFILIATEID}&site=FANZA&service=ebook&floor=comic&articleoutput=json'
response = requests.get(genre_url)
genre_text = response.text
p = response.json()
genre_data = json.loads(genre_text)
genre_item = genre_data['result']['items']


pprint.pprint(genre_item)

# initial=%E3%81%99& スパンキング

"""オールジャンル取得"""
# all_genre = requests.get(f'https://api.dmm.com/affiliate/v3/GenreSearch?api_id={APIID}&affiliate_id={AFFILIATEID}&floor_id=43&hits=500&offset=1&output=json')
# all_genre_text = all_genre.text
# all_genre_data = json.loads(all_genre_text)
# all_genre_item = all_genre_data['result']

# with open('genre.json', 'w', encoding='utf-8') as f:
#     json.dump(all_genre_item, f, indent=4, ensure_ascii=False)

class Genre_read:

    """ジャンルのIDを取得する"""
    def jsonload(self):
        with open('genre.json', 'r', encoding='utf-8') as r:
            genre = json.load(r)
            for items in genre['genre']:
                if 'スパンキング' in items['name']:
                    page_url = items['list_url']
                    print(page_url)
        return page_url


    """ジャンルに特化した最新の動画を集める"""


    def genre_get_movie(self):
        hits_count = 20
        offset_count = 1

        """ジャンルID
        スパンキング: 6940
        辱め： 27
        鼻フック： 6950
        """

        genre_id = 6950

        while True:
            genre_url = f'https://api.dmm.com/affiliate/v3/ItemList?api_id={APIID}&affiliate_id={AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits={hits_count}&sort=date&offset={offset_count}&article=genre&article_id={genre_id}&output=json'
            response = requests.get(genre_url)
            genre_text = response.text
            genre_data = json.loads(genre_text)
            genre_item = genre_data['result']['items']


            for items in genre_item:
                try:
                    average = items['review']['average']
                    if float(average) >= 3.5:
                        af_url = items['affiliateURL']
                        title = items['title']
                        videos_info = items['sampleMovieURL']
                        del videos_info['pc_flag'], videos_info['sp_flag']

                        size_array = []
                        video_array = []
                        for size, v_url in videos_info.items():

                            max_size_info = size.split('_')
                            split_size = int(max_size_info[1])
                            size_array.append(split_size)
                            video_array.append(v_url)

                        max_size = size_array.index(max(size_array))
                        if str(size_array[max_size]) in v_url:

                            if videos_info:
                                yield dict(
                                    title=title,
                                    aff_url=af_url,
                                    video_url=v_url
                            )
                except Exception as ex:
                    print(ex)

            offset_count = hits_count + offset_count

            if len(genre_item) == 0:
                break

        with open('genre.json', 'w', encoding='utf-8') as f:
            json.dump(all_genre_item, f, indent=4, ensure_ascii=False)


class video:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36')
        self.driver = webdriver.Chrome('C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe', options=self.options)
        # self.driver = webdriver.Chrome(options=self.options)  #options=self.options 'C:\\Users\\PC_User\\Documents\\GitHub\\kutikomi\\bakusai\\chromedriver.exe'
        #self.driver.implicitly_wait(10)

        self.wait = WebDriverWait(driver=self.driver, timeout=30)

    def down(self, index, video_info: dict):

        print(video_info)
        self.driver.get(video_info['video_url'])
        self.wait.until(EC.presence_of_all_elements_located)
        iframe = self.driver.find_element(by=By.TAG_NAME, value='iframe')
        self.driver.switch_to.frame(iframe)
        elem = self.driver.find_element(by=By.XPATH, value="//main[contains(@id, 'dmmvideo-player')]/video").get_attribute('src')
        print(elem)

        video_response = requests.get(elem)
        with open(f'{index}test.mp4', 'wb') as save_v:
            save_v.write(video_response.content)


if __name__ == '__main__':

    zz = Genre_read()
    vv = video()
    for i, video_info in enumerate(zz.genre_get_movie()):
        vv.down(i, video_info)
