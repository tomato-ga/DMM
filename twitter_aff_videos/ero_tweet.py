
import tweepy
import API_config_katudon
import requests
from bs4 import BeautifulSoup
import re



class Tweet_get:

    auth = tweepy.OAuthHandler(API_config_katudon.API_KEY, API_config_katudon.API_SECRET)
    auth.set_access_token(API_config_katudon.ACCESS_TOKEN, API_config_katudon.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # search_result = tweepy.Cursor(api.user_timeline, screen_name=key_account, include_rts=False, include_entities=True, tweet_mode='extended', lang='ja').items(10)
    # print(search_result)

    """投稿IDによってスレッドとスレッドじゃない場合がある
    最初に読み込むツイートでvideo URLを含まないツイートが存在するのでifできりわける？"""

    @classmethod
    def url_get(self, key_accounts) -> list:

        count_no = 5
        key_account = key_accounts
        account_id = str(key_account.replace('https://twitter.com/', ''))
        results: iter = tweepy.Cursor(self.api.user_timeline, # タイムラインの取得
                    id=account_id, # 取得対象のユーザーを指定
                    include_entities=True, # 省略されたリンクを全て取得
                    tweet_mode='extended', # 省略されたツイートを全て取得
                    lang='ja',
                    exclude_replies=False,
                    include_rts=False).items(count_no) # 取得件数を指定 .pages()でもいける

        video_urls_list = []
        af_urls_list = []



        for result in results:
            try:
                """スレッドのうしろから取る場合"""
                moto_tweet_id = result.in_reply_to_status_id
                text_urls = result.entities['urls']

                """スレッドの場合、元ツイートの動画を取得"""
                moto_tweet = self.api.get_status(moto_tweet_id, include_entities=True)
                moto_medias = moto_tweet.extended_entities['media']

                if 'video_info' in moto_medias[0]:
                    ex_media_video_variants = moto_medias[0]['video_info']['variants']

                    bitrate_array = []
                    for movie in ex_media_video_variants:
                        bitrate_array.append(movie.get('bitrate',0))
                    max_index = bitrate_array.index(max(bitrate_array))
                    movie_url = ex_media_video_variants[max_index]['url']

                    if movie_url:
                        video_urls_list.append(movie_url)

                """DMM or MGSのURL取得"""
                for urls in text_urls:
                    af_url = urls['expanded_url']
                    print(af_url)
                    if af_url:
                        af_urls_list.append(af_url)


            except Exception as ex:
                """スレッドの前からとる場合、動画URLとって、スレッドconvarsation?のIDを取得"""
                print('[url_get]: Exception:', ex)
                pass


        return video_urls_list, af_urls_list


    @classmethod
    def video_af_url_get(self, v_url_list, af_url_list):

        for i, (v_url, af_url) in enumerate(zip(v_url_list, af_url_list)):
            response = requests.get(v_url)
            v_url_file_name_list = re.findall('(/[a-zA-z0-9_-]*)(.mp4)', v_url)
            v_url_file_name = v_url_file_name_list[0][0]
            v_url_file_name = v_url_file_name.replace('/', '')
            with open(f'E:\\Dropbox\\Download\\{str(v_url_file_name)}{i}.mp4', 'wb') as save_video:
                save_video.write(response.content)

            if 'dmm' in af_url:
                urls =re.sub('[a-zA-z0-9]*-\d{3}', 'kamipanmen-001',  af_url)
                print('[video_af_url_get]:', urls)
            elif 'mgs' in af_url:
                urls = re.sub('[^_=.*?][A-Z0-9*]{25}', 'R2YZBPJ6L7WYGJYWOPG8NJAMRY', af_url)
                print('[video_af_url_get]:', urls)
            else:
                pass

            print(dict(index=i, video_file=f'{str(v_url_file_name)}{i}.mp4', url=urls))


if __name__ == '__main__':
    i = Tweet_get()
    key_accounts = 'https://twitter.com/paipai1414'
    video_urls_list, af_urls_list = i.url_get(key_accounts)
    i.video_af_url_get(video_urls_list, af_urls_list)




#TODO 1, 404 No Statusの原因探し printで確認する
#TODO 2, 全件取得し、ファイル名とアフィURLをDBに保存する
#TODO 3, MongoDBメソッド用意

"""
正規表現でアフィID特定完了
# https://al.dmm.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdigital%2Fvideoa%2F-%2Fdetail%2F%3D%2Fcid%3Dssis00253%2F&af_id=totokyu2019-001
# af._?id=[0-9a-zA-Z_].* → af_id=totokyu2019-001の部分がとれるので、それを置き換える

【DMM】
[a-zA-z0-9]*-\d{3} ←これでDMM ID全部取れるため、re.subで置換する

【MGS】
[^_=.*?][A-Z0-9*]{25}
26だと取れなかった。25にして、アンダーバーとイコールを削除
"""
