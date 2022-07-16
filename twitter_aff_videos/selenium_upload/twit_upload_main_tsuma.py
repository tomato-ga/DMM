from master_twit_upload_module_genre_qwpo import Tweet
import json
import pandas as pd
import random
import os

"""
【使い方】
jsonとファイルディレクトリとaccountを指定する
"""

if __name__ == '__main__':
    load_json = json.load(open('/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_tsuma_videofile.json')),
    l = random.sample(load_json, 1)

    df = pd.DataFrame.from_dict(l)
    random_video = df.sample()
    upload_video_dict: dict = random_video.values[0][0]
    upload_video_random = random.sample(upload_video_dict, 1)
    upload_url: str = upload_video_random[0]['aff_url']
    upload_title: str = upload_video_random[0]['title']
    upload_file_name: str = upload_video_random[0]['cut_file_name']
    upload_path_and_file_name: str = '/mnt/hdd/don/files/fanza/tsuma_cut/' + upload_file_name
    assert os.path.isfile(upload_path_and_file_name)
    print(upload_path_and_file_name, ':', upload_url, upload_title)

    i = Tweet()
    i.Uploads(account='tsuma_doga', up_file=upload_path_and_file_name, text=upload_title)
    i.Quit()


"""
履歴
2022/05/23 0:44
textとup_urlを削除
フォロワー増えるまで消しておく

bust90to99のファイルがないので停止

2022/05/23 20:24
assert追加ファイル確認

2022/07/16 23:47
tsuma新規追加
"""