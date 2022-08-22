import tweepy
import API_config_1oku
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

    def url_get(self, key_account: str) -> list:
        """
        key_account(str): twitter IDを解析する

        [Handle Rate Limits] wait_on_rate_limit https://docs.tweepy.org/en/stable/examples.html#examples
        これは、クエリ "Twitter" を含むツイートを検索し、最大で次のものを返します。
        Twitter APIへの1回のリクエストにつき最大100ツイートまで
        レートリミットに達すると、自動的に待機/スリープ状態になります。"""

        count_no = 3000
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
                    moto_tweet = self.api.get_status(moto_tweet_id, include_entities=True, tweet_mode='extended')
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

                    """もしスレッドじゃなかったら"""
                elif not result.in_reply_to_status_id:
                    # URLとる
                    text_urls = result.entities['urls']
                    comment = result.full_text

                    """DMM or MGSのURL取得"""
                    for urls in text_urls:
                        af_url = urls['expanded_url']
                        print(af_url)
                        if af_url:
                            af_urls_list.append(af_url)

                    # 動画URLとる
                    moto_medias = result.extended_entities['media']

                    if 'video_info' in moto_medias[0]:
                        ex_media_video_variants = moto_medias[0]['video_info']['variants']

                        bitrate_array = []
                        for movie in ex_media_video_variants:
                            bitrate_array.append(movie.get('bitrate',0))
                        max_index = bitrate_array.index(max(bitrate_array))
                        movie_url = ex_media_video_variants[max_index]['url']

                        if movie_url:
                            video_urls_list.append(movie_url)

                        yield (dict(video_url=movie_url, af_url=af_url, comment=comment, id=account_id))


                else:
                    pass

            except Exception as ex:
                print('[url_get]: Exception:', ex)
                pass


    def video_af_url_get(self,movie_url, af_url, comment, account_id, tag) -> list:
        """動画のファイル名、アフィリエイトURL、ツイッターのテキスト、元のIDを保存する

        Args:
            movie_url (_type_): _description_
            af_url (_type_): _description_
            comment (_type_): _description_
            account_id (_type_): _description_

        Returns:
            list: _description_
        """

        response = requests.get(movie_url)
        v_url_file_name_list = re.findall('(/[a-zA-z0-9_-]*)(.mp4)', movie_url)
        v_url_file_name = v_url_file_name_list[0][0]
        v_url_file_name = v_url_file_name.replace('/', '')
        with open(f'/mnt/hdd/don/files/twitvideo_sio/{str(v_url_file_name)}.mp4', 'wb') as save_video:
            save_video.write(response.content)
            time.sleep(2)

        if 'dmm' in af_url:
            urls =re.sub('[a-zA-Z0-9]*-\d{3}', 'kamipanmen-001',  af_url)
            print('[video_af_url_get]:', urls)
        elif 'mgs' in af_url:
            urls = re.sub('[^_=.*?][A-Z0-9*]{25}', 'R2YZBPJ6L7WYGJYWOPG8NJAMRY', af_url)
            print('[video_af_url_get]:', urls)
        else:
            urls = ""

        now = datetime.datetime.today()
        video_info = dict(video_file=f'{str(v_url_file_name)}.mp4', url=urls, comment=comment, id=account_id, tag=tag, time=now)

        self.save_db(video_info)


    def info_matome(self, key_accounts: list, tag):
        """
        video_af_url_getにパース情報を渡す

        Args:
            key_accounts (list): TwitterアカウントをURLのリストで渡す
        """
        for key_account in key_accounts:
            dicts = self.url_get(key_account)
            for info in dicts:
                movie_url = info['video_url']
                af_url = info['af_url']
                comment = info['comment']
                account_id = info['id']

                self.video_af_url_get(movie_url, af_url, comment, account_id, tag)

    def db_set(self):
        db_url = 'mongodb://pyton:radioipad1215@192.168.0.25:27017'
        client = pymongo.MongoClient(db_url)
        db = client.twitter
        collection = db.sio

        return collection


    def save_db(self, video_info):
        collection = self.db_set()
        collection.insert_one(video_info)


if __name__ == '__main__':

    key_accounts = [
        # 'https://twitter.com/k9xypip',
        # 'https://twitter.com/cb_Eugene13',
        # 'https://twitter.com/penne27436851',
        # 'https://twitter.com/beauty_pretty_i',
        # 'https://twitter.com/SGmRmu3SzDfvshj',
        # 'https://twitter.com/reiwachijo', # とれない
        # 'https://twitter.com/Erotube081',
        # 'https://twitter.com/tmp_pnpk',s
        # 'https://twitter.com/Spelunker1231',
        # 'https://twitter.com/Mature_Milf_Mom',
        # 'https://twitter.com/AV_honpo_kyonyu' #巨乳
        # 'https://twitter.com/1919com1919',
        # 'https://twitter.com/kekooharenchi',
        # 'https://twitter.com/er_oyaji', #取得済み
        # 'https://twitter.com/moemoelover_s' #取得済み
        # 'https://twitter.com/kyosyashima'
        # 'https://twitter.com/paiotuseizin',
        # 'https://twitter.com/SGmRmu3SzDfvshj'
        # あとで！！！！！！！！！！！！！'https://twitter.com/chikubi0909'
        # 'https://twitter.com/wataru_erobakka'
        # スレッドじゃないからとれなかった"https://twitter.com/SeibiSenmon"
        # スレッドだけど引用してるからとれなかった"https://mobile.twitter.com/Myra98544314"
        # "https://twitter.com/k_tzip" OK
        # 'https://twitter.com/SeibiSenmon' OK
        # "https://twitter.com/Myra98544314"
        # "https://twitter.com/ikaseifuku"
        # "https://twitter.com/sefu9girl"
        # "https://twitter.com/AV_honpo_kyonyu",
        # "https://twitter.com/pahupahu0909",
        # "https://twitter.com/GALS1collection",
        # "https://twitter.com/ero_gal_girls",
        # "https://twitter.com/gal3150_movie"
        "https://twitter.com/tadanoHauthor",
        "https://twitter.com/funshagirls",
        "https://twitter.com/kame_hame8102",
        "https://twitter.com/funsha_megami"


    ]

    tag = "潮吹き"

    i = Tweet_get()
    i.info_matome(key_accounts, tag)



#TODO , key_accountsを辞書にしてtypeを追加する ex, 'type': 'sirouto' 'type': 'normal' etc...


"こっち"
"""ダウンロードリスト　ジャンル別"""
"素人"

'https://twitter.com/sirouto_douga_h'
'https://twitter.com/shiroutotyan'


"good"
"https://twitter.com/EROSCOUTER",
"https://twitter.com/yoru__tomo"
"https://twitter.com/MGS0909"
"https://twitter.com/av_samurai4545"
"https://twitter.com/ero_dou_"


"tikubi"
'https://twitter.com/chikubi0909'


"gal"
"ギャルはtwitvideo2へ"



"尻"
"https://twitter.com/osiri_no_kuni"
"https://twitter.com/hdougasuki"
"https://twitter.com/dadadada511"
"https://twitter.com/osidanprpr"


"潮吹き"




"巨乳"
"https://twitter.com/paimori69"


# "制服"
# "https://twitter.com/SeibiSenmon"
# "https://mobile.twitter.com/Myra98544314"
# "https://mobile.twitter.com/k_tzip"
# "https://mobile.twitter.com/ikaseifuku"
# "https://twitter.com/sefu9girl"


"足"
"https://mobile.twitter.com/asi_pansuto"