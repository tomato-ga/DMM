from master_twit_upload_module_genre import Tweet
import json
import pandas as pd


"""イラマ・スパンキング特化"""

if __name__ == '__main__':

    load_json = json.load(open('/home/don/py/DMM/DMMAPI/fanza_genreイラマチオ_videofile.json'))
    print(len(load_json['title']))

    df = pd.DataFrame.from_dict(load_json)
    random_video = df.sample()
    upload_video_dict: dict = random_video.values[0][0]
    upload_url: str = upload_video_dict['aff_url']
    upload_file_name: str = upload_video_dict['file_name']
    upload_path_and_file_name = '/mnt/hdd/don/files/fanza/hazukasi/' + upload_file_name
    print(upload_file_name, ':', upload_url)

    i = Tweet()
    i.Uploads(account='OtxSf', text='今日はこれでぬきぬき！', up_url=upload_url, up_file=upload_path_and_file_name)
    i.Quit()
