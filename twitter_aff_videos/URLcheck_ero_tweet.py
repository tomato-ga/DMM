
import tweepy
import API_config_katudon
import requests
import re
import pymongo
import time
import datetime


class Tweet_get:
    #WARN katudonのAPI使ってるのに注意する 200万/月アクセス可能 Elevated
    auth = tweepy.OAuthHandler(API_config_katudon.API_KEY, API_config_katudon.API_SECRET)
    auth.set_access_token(API_config_katudon.ACCESS_TOKEN, API_config_katudon.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # search_result = tweepy.Cursor(api.user_timeline, screen_name=key_account, include_rts=False, include_entities=True, tweet_mode='extended', lang='ja').items(10)
    # print(search_result)

    """
    1.投稿IDによってスレッドとスレッドじゃない場合がある
    最初に読み込むツイートでvideo URLを含まないツイートが存在するのでifできりわける？
    →スレッドだけ取得して、元のツイートIDに遡ってvideo獲得した

    2.正規表現でアフィID特定完了
    # https://al.dmm.co.jp/?lurl=https%3A%2F%2Fwww.dmm.co.jp%2Fdigital%2Fvideoa%2F-%2Fdetail%2F%3D%2Fcid%3Dssis00253%2F&af_id=totokyu2019-001
    # af._?id=[0-9a-zA-Z_].* → af_id=totokyu2019-001の部分がとれるので、それを置き換える

    【DMM】
    [a-zA-z0-9]*-\d{3} ←これでDMM ID全部取れるため、re.subで置換する

    【MGS】
    [^_=.*?][A-Z0-9*]{25}
    26だと取れなかった。25にして、アンダーバーとイコールを削除
    """

    def url_get(self, key_account) -> list:

        """[Handle Rate Limits] wait_on_rate_limit https://docs.tweepy.org/en/stable/examples.html#examples
        これは、クエリ "Twitter" を含むツイートを検索し、最大で次のものを返します。
        Twitter APIへの1回のリクエストにつき最大100ツイートまで
        レートリミットに達すると、自動的に待機/スリープ状態になります。"""

        count_no = 3
        video_urls_list = []
        af_urls_list = []
        comments_list = []


        account_id = str(key_account.replace('https://twitter.com/', ''))

        results: iter = tweepy.Cursor(self.api.user_timeline, # タイムラインの取得
                    id=account_id, # 取得対象のユーザーを指定
                    include_entities=True, # 省略されたリンクを全て取得
                    tweet_mode='extended', # 省略されたツイートを全て取得
                    lang='ja',
                    exclude_replies=False,
                    include_rts=False).items(limit=count_no) # 取得件数を指定


        for result in results:
            try:
                """スレッドのうしろから取る場合"""
                if result.in_reply_to_status_id:
                    moto_tweet_id = result.in_reply_to_status_id
                    text_urls = result.entities['urls']
                    comment = result.full_text
                    comments_list.append(comment)

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

                        yield (dict(video_url=movie_url, af_url=af_url, comment=comment, id=account_id))

            except Exception as ex:
                """スレッドの前からとる場合、動画URLとって、スレッドconvarsation?のIDを取得"""
                print('[url_get]: Exception:', ex)
                pass



        # return video_urls_list, af_urls_list, comments_list,  # TODO 1.yieldで返すようにする：リストをやめる key_account AVのタイプを保存しておきたい 2.元ツイートURLとツイートauthor_idを保存する


    def video_af_url_get(self,movie_url, af_url, comment, account_id) -> list:

        # video_lists = []

        response = requests.get(movie_url)
        v_url_file_name_list = re.findall('(/[a-zA-z0-9_-]*)(.mp4)', movie_url)
        v_url_file_name = v_url_file_name_list[0][0]
        v_url_file_name = v_url_file_name.replace('/', '')
        with open(f'E:\\twitvideo\\{str(v_url_file_name)}.mp4', 'wb') as save_video:   # Ubuntu /mnt/hdd/don/files //  Win f'E:\\twitvideo\\{str(v_url_file_name)}.mp4',
            save_video.write(response.content)
            time.sleep(2)

        if 'dmm' in af_url:
            urls =re.sub('[a-zA-Z0-9]*-\d{3}', 'kamipanmen-001',  af_url)
            print('[video_af_url_get]:', urls)
        elif 'mgs' in af_url:
            urls = re.sub('[^_=.*?][A-Z0-9*]{25}', 'R2YZBPJ6L7WYGJYWOPG8NJAMRY', af_url)
            print('[video_af_url_get]:', urls)
        else:
            pass


        now = datetime.datetime.today()
        # video_lists.append(dict(video_file=f'{str(v_url_file_name)}.mp4', url=urls, comment=comment, id=account_id, time=now))

        # return video_lists

        video_info = dict(video_file=f'{str(v_url_file_name)}.mp4', url=urls, comment=comment, id=account_id, time=now)

        self.save_db(video_info)


    def info_matome(self, key_accounts):
        for key_account in key_accounts:
            dicts = i.url_get(key_account)
            for info in dicts:
                movie_url = info['video_url']
                af_url = info['af_url']
                comment = info['comment']
                account_id = info['id']

                self.video_af_url_get(movie_url, af_url, comment, account_id)

    def db_set(self):
        db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
        client = pymongo.MongoClient(db_url)
        db = client.twitter
        collection = db.testtest

        return collection


    def save_db(self, video_info):
        collection = self.db_set()
        collection.insert_one(video_info)



if __name__ == '__main__':

    key_accounts = [
        'https://twitter.com/k9xypip',
        'https://twitter.com/paipai1414',
        # 'https://twitter.com/cb_Eugene13',
        # 'https://twitter.com/penne27436851',
        # 'https://twitter.com/beauty_pretty_i',
        # 'https://twitter.com/SGmRmu3SzDfvshj',
        # 'https://twitter.com/reiwachijo',
        # 'https://twitter.com/Erotube081',
        # 'https://twitter.com/tmp_pnpk',
        # 'https://twitter.com/Spelunker1231',
        # 'https://twitter.com/nukitender',
        # 'https://twitter.com/Mature_Milf_Mom',
        # 'https://twitter.com/AV_honpo_kyonyu' #巨乳
    ]

    i = Tweet_get()
    i.info_matome(key_accounts)



#TODO , key_accountsを辞書にしてtypeを追加する ex, 'type': 'sirouto' 'type': 'normal' etc...
#TODO , dbとpandasで差分取得する
