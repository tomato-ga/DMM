import os
import json
import requests
import time
import datetime
from box import Box
from dataclasses import dataclass
import pandas as pd


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from master_movie_5secounds_cut import Cut
from master_fanza_download_from_json import Video_download


@dataclass
class Genre_dmm:

    APIID: str = ''
    AFFILIATEID: str = ''
    keyword: str = ''
    offset_count: int = 0
    hits_count = 0
    old_titles_json = None

    # floor =  requests.get(f'https://api.dmm.com/affiliate/v3/FloorList?api_id={APIID}&affiliate_id={AFFILIATEID}&output=json')

    #pprint.pprint(Box.from_json(floor.text))
    # json_box = Box.from_json(floor.text)
    # print(json_box)


    @property
    def search_keyword(self):

        print(self.old_titles_json)
        search_response = {}
        search_response['title'] = []

        while True:
            search_keyword_response = requests.get(f'https://api.dmm.com/affiliate/v3/ItemList?api_id={self.APIID}&affiliate_id={self.AFFILIATEID}&site=FANZA&service=digital&floor=videoa&hits={self.hits_count}&sort=rank&keyword={self.keyword}&offset={self.offset_count}&output=json')
            time.sleep(0.2)
            search_json_box = Box.from_json(search_keyword_response.text)
            items = search_json_box.result['items']
            print(type(items))
            print(dir(items))

            for item in items:
                if item['title'] not in self.old_titles_json:
                    try:
                        average = item.review.average
                        if float(average) >= 4:
                            af_url = item.affiliateURL
                            title = item.title
                            video_info = item.sampleMovieURL
                            video_date = item.date
                            del video_info.pc_flag, video_info.sp_flag

                            if video_info:
                                size_array = []
                                video_array = []
                                for size, v_url in video_info.items():

                                    max_size_info = size.split('_')
                                    split_size = int(max_size_info[1])
                                    size_array.append(split_size)
                                    video_array.append(v_url)

                                max_size = size_array.index(max(size_array))
                                search_response['title'].append(item.to_dict())

                                if str(size_array[max_size]) in v_url:
                                    if video_info:
                                        yield dict(
                                            title=title,
                                            aff_url=af_url,
                                            video_url=v_url,
                                            date=video_date
                                    )

                    except Exception as ex:
                        print(ex)


                elif item['title'] in self.old_titles_json:
                    print('JSONにあるitemです')
                    pass


            self.offset_count = self.hits_count + self.offset_count



            if len(items) == 0:
                with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_{self.keyword}.json', 'w+', encoding='utf-8') as f:
                    json.dump(search_response, f, indent=4, ensure_ascii=False)
                break



if __name__ == '__main__':

    g = Genre_dmm()
    g.APIID = 'b7fkZaG3pW6ZZHpGBbLz'
    g.AFFILIATEID = 'kamipanmen-990'
    g.keyword= 'スパンキング'
    file_and_json_name = 'spanking'
    g.offset_count = 1
    g.hits_count = 80

    old_json = json.load(open(f'/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_{file_and_json_name}_videofile.json', 'r'))
    old_df = pd.DataFrame(old_json['title'])
    old_titles = old_df['title'].tolist()
    g.old_titles_json = old_titles

    save_json = {}
    save_json['title'] = []
    for i, video_info in enumerate(g.search_keyword):
        print(i, video_info)
        save_json['title'].append(video_info)
        old_json['title'].append(video_info)
        # todo old_jsonにvideo_infoを追加する↑ save_jsonみたいなやつ

    with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_old_{g.keyword}.json', 'w+', encoding='utf-8') as f:
        json.dump(old_json, f, indent=4, ensure_ascii=False)
    with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_new_{g.keyword}.json', 'w+', encoding='utf-8') as f:
        json.dump(save_json, f, indent=4, ensure_ascii=False)


    # 新しいファイルのダウンロード実行
    load_json = json.load(open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_new_{g.keyword}.json'))
    print(f"ダウンロード件数は: {len(load_json['title'])}です")

    save_json = {}
    save_json['title'] = []

    vv = Video_download()
    for i, video_info in enumerate(load_json['title']):
        print(i, video_info)
        try:
            new_video_info = vv.down(index=i, video_info=video_info, file_name=file_and_json_name)
            if new_video_info:
                save_json['title'].append(new_video_info)
                time.sleep(0.2)
        except Exception as ex:
            print(ex)
            pass

    with open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_{file_and_json_name}_videofile.json', 'w+', encoding='utf-8') as f:
        json.dump(save_json, f, indent=4, ensure_ascii=False)


    # ダウンロードしたファイルのカット実行
    c = Cut()
    file_dir = f'/mnt/hdd/don/files/fanza/{file_and_json_name}/'
    cut_file_dir = f'/mnt/hdd/don/files/fanza/{file_and_json_name}_cut/'
    cut_file_name = f'{file_and_json_name}_cut_{str(datetime.date.today())}'
    c.name = g.keyword
    c.json_name = file_and_json_name

    if os.path.exists(cut_file_dir) is False:
        os.makedirs(cut_file_dir, exist_ok=True)

    load_json_dict = json.load(open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_{file_and_json_name}_videofile.json'))
    print(len(load_json_dict['title']))
    load_json_cut = load_json_dict['title']
    assert type(load_json_cut) == list

    c.again_cut5seconds(file_dir, cut_file_dir, cut_file_name, load_json_cut)

"""
履歴
2022/06/10 20:21
定期取得のために、①old_jsonをmasterへ変更②Cutクラスでagain用のメソッド追加

# TODO ビデオサイズが小さいファイルを再度ダウンロードしているため、notdownload_jsonなどを作って待避させるようにする 
# ↑ 2022/07/03？？？
"""