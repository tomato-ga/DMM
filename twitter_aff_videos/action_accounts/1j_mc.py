import tweepy
import api_1j_mc
import time
import random


wait = random.uniform(10, 25)
wait_long = random.uniform(30, 50)

def Thirdparty_rt():
    """他者アカウント"""


    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_1j_mc.API_KEY, consumer_secret=api_1j_mc.API_SECRET, access_token=api_1j_mc.ACCESS_TOKEN, \
        access_token_secret=api_1j_mc.ACCESS_TOKEN_SECRET, bearer_token=api_1j_mc.Bearer_token)

    # リストのツイート取得 非公開リストは取得NG 公開設定にする
    response = client.get_list_tweets(id=1514978714572173313, max_results=15,  expansions=["attachments.media_keys","author_id","referenced_tweets.id"], tweet_fields=["context_annotations","public_metrics","created_at", "text", "source", "geo"])
    tweet = response.data
    random.shuffle(tweet)
    print(tweet)


    rt_count = 0
    while rt_count < 3:
        for media in tweet:
            mediatw = media.data
            if 'attachments' in mediatw: #動画つきのツイートだけに絞り込む
                post = media.id # 動画つきのツイートのIDだけ抜き出す
                time.sleep(wait)
                try:
                    client.retweet(post) # 自動RT
                    rt_count += 1
                    if rt_count == 3:
                        break
                except Exception as e:
                    print(e)
                else:
                    print('RT完了')

def My_rt():

    """自分アカウントの公式リツイートだけ"""

    client = tweepy.Client(consumer_key=api_1j_mc.API_KEY, consumer_secret=api_1j_mc.API_SECRET, access_token=api_1j_mc.ACCESS_TOKEN, \
        access_token_secret=api_1j_mc.ACCESS_TOKEN_SECRET, bearer_token=api_1j_mc.Bearer_token)

    """自分アカウント"""

    ids: list = [
        1515696887781015558,
        1515697390480945160,
        1515978583730458630
    ]


    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=5, exclude='retweets', expansions=["attachments.media_keys","author_id","referenced_tweets.id"], tweet_fields=["context_annotations","created_at","text","source","entities"])
            name: list = [username_0.data['username'] for username_0 in timeline.includes['users']]
            username =name[0]

            rts_tweet = timeline.data
            random.shuffle(rts_tweet)
            print(rts_tweet)
        except Exception as ex:
            print(ex)
            pass


        for rt_tweet in rts_tweet:
            rttw = rt_tweet.data
            if 'attachments' in rttw:
                post_mine = rt_tweet.id
                time.sleep(wait)
                try:
                    client.retweet(post_mine)
                except Exception as e:
                    print(e)
                else:
                    print('自分のRTとReply完了!!')


Thirdparty_rt()
My_rt()
