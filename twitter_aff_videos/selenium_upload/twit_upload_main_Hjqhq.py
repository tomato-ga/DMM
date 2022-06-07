from master_twit_upload_module_genre import Tweet
import json
import pandas as pd
import random
import os


if __name__ == '__main__':
    load_json = {
        "f_cup": json.load(open('/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_f_cup_videofile.json')),
        "g_cup": json.load(open('/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_g_cup_videofile.json')),
        "h_cup" : json.load(open('/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_h_cup_videofile.json')),
    }
    l = random.choice(list(load_json.items()))
    type_l = l[0]
    dict_l = random.sample(l[1]["title"], 1)

    upload_url: str = dict_l[0]['aff_url']
    upload_title: str = dict_l[0]['title']
    upload_file_name: str = dict_l[0]['cut_file_name']

    match type_l:
        case 'f_cup':
            upload_path_and_file_name: str = '/mnt/hdd/don/files/fanza/f_cup_cut/' + upload_file_name
        case 'g_cup':
            upload_path_and_file_name: str = '/mnt/hdd/don/files/fanza/g_cup_cut/' + upload_file_name
        case 'h_cup':
            upload_path_and_file_name: str = '/mnt/hdd/don/files/fanza/h_cup_cut/' + upload_file_name

    assert os.path.isfile(upload_path_and_file_name)
    print(upload_path_and_file_name, ':', upload_url)

    i = Tweet()
    i.Uploads(account='HjQhq', up_file=upload_path_and_file_name, text=upload_title)
    i.Quit()


"""
履歴
2022/05/23 0:44
textとup_urlを削除
フォロワー増えるまで消しておく

bust90to99のファイルがないので停止

2022/05/23 20:24
assert追加ファイル確認


2022/06/07 15:31
f-g-hのどれかをランダムに取得
match caseで当てはまるタイプを選択
"""