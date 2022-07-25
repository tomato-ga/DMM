from moviepy.editor import *
import os
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import shutil

@dataclass
class Cut:

    name = ''
    json_name = ''

    def cut5secounds(self, file_directory, cut_file_directory, cut_file_name, load_json_dict):
        """_summary_

        Args:
            file_directory (_type_): ファイルパス取得時に使用
            cut_file_directory (_type_): カットしたファイルの保存ディレクトリ
            cut_file_name (_type_): カットしたファイルの名前
            load_json_dict (_type_): jsonを読み込んでファイル名を取得
            names (_type_): master json保存に使用
        """
        save_json = {}
        save_json['title'] = []
        for i, video_info in enumerate(load_json_dict, start=1): # TODO JSONをforで回してファイル名取得→os.pathでファイル名を取得してcut処理をするように変更する

            file = os.path.abspath(file_directory + video_info['file_name'])
            #ビデオパスを入れる（保存先パスとファイル名になる）
            save_file_name = f'{cut_file_directory}{i}_{cut_file_name}.mp4'
            start = 5

            try:
                videos = VideoFileClip(file).subclip(start)
                a = videos.write_videofile(save_file_name, fps=29, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
                video_info['cut_file_name'] = f'{i}_{cut_file_name}.mp4'
                save_json['title'].append(video_info)
                print(f'カット完了', {video_info['title']})
            except Exception as ex:
                print(ex)
                pass

        with open(f'/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_{self.name}_videofile.json', 'w+', encoding='utf-8') as f:
            json.dump(save_json, f, indent=4, ensure_ascii=False)

        # もしカットしたら、ダウンロードフォルダを削除する。カット終了の値を取得する↑
        if os.path.exists(file_directory):
            shutil.rmtree(file_directory)


    def again_cut5seconds(self, file_directory, cut_file_directory, cut_file_name, load_json_dict):
        """_summary_

        Args:
            file_directory (_type_): ファイルパス取得時に使用
            cut_file_directory (_type_): カットしたファイルの保存ディレクトリ
            cut_file_name (_type_): カットしたファイルの名前
            load_json_dict (_type_): jsonを読み込んでファイル名を取得
            names (_type_): master json保存に使用
        """
        save_json = {}
        save_json['title'] = []
        for i, video_info in enumerate(load_json_dict, start=1): # TODO JSONをforで回してファイル名取得→os.pathでファイル名を取得してcut処理をするように変更する

            file = os.path.abspath(file_directory + video_info['file_name'])
            #ビデオパスを入れる（保存先パスとファイル名になる）
            save_file_name = f'{cut_file_directory}{i}_{cut_file_name}.mp4'
            start = 5

            try:
                videos = VideoFileClip(file).subclip(start)
                a = videos.write_videofile(save_file_name, fps=29, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
                video_info['cut_file_name'] = f'{i}_{cut_file_name}.mp4'
                save_json['title'].append(video_info)
                print(f'カット完了', {video_info['title']})
            except Exception as ex:
                print(ex)
                pass

        master_json = json.load(open(f'/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_{self.json_name}_videofile.json'))

        if len(save_json['title']) != 0:
            try:
                for i in save_json['title']:
                    print(i)
                    master_json['title'].append(i)

                with open(f'/home/don/py/DMM/DMMAPI/JSON/master_fanza_genre_{self.json_name}_videofile.json', 'w+', encoding='utf-8') as f:
                    json.dump(master_json, f, indent=4, ensure_ascii=False)

                # もしカットしたら、ダウンロードフォルダを削除する。カット終了の値を取得する↑
                if os.path.exists(file_directory):
                    shutil.rmtree(file_directory)

            except Exception as ex:
                print('cut', ex)
                pass

        else:
            print("カットファイルはありません。終了しました")
            pass



    def cut2min():
        video_path = '/Users/ore/Downloads/[FRIDAY] Risa Yukihira 雪平莉左 - Do you like a beautiful older sister 綺麗なお姉さんは、好きですか？ (2021-11-18)/yukihira.ts' #ビデオパスを入れる
        save_file_name = 'cuttest.mp4' #保存ファイル名
        start = 5

        videos = VideoFileClip(video_path).subclip(start)
        videos.write_videofile(save_file_name, fps=29)

"""
使い方
①namesに名前をテーマっぽいのをいれる
②file_dirに動画保存してるディレクトリをいれる
③cut_file_dirにカットした動画の保存先ディレクトリを入れる

"""

######## WARNING クラスにする前の処理↓
# name = 'anal'
# file_dir = f'/mnt/hdd/don/files/fanza/{name}/'
# cut_file_dir = f'/mnt/hdd/don/files/fanza/{name}_cut/'
# cut_file_name = f'{name}_cut'

# if os.path.exists(cut_file_dir) is False:
#     os.makedirs(cut_file_dir, exist_ok=True)

# load_json_dict = json.load(open(f'/home/don/py/DMM/DMMAPI/JSON/fanza_genre_{name}_videofile.json'))
# print(len(load_json_dict['title']))

# cut5secounds(file_dir, cut_file_dir, cut_file_name, load_json_dict['title'], name)

"""
履歴
2022/06/02 22:06
クラス化して、処理をmaster_fanza_genre_get_movie_urlにimportさせた

2022/06/06 23:05
カット終了後、ダウンロードフォルダを削除

"""