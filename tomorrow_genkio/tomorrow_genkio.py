import tweepy
import api_tomorrow_genkio
import time
import random


def tweet():
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_tomorrow_genkio.API_KEY, consumer_secret=api_tomorrow_genkio.API_SECRET, access_token=api_tomorrow_genkio.ACCESS_TOKEN, \
        access_token_secret=api_tomorrow_genkio.ACCESS_TOKEN_SECRET, bearer_token=api_tomorrow_genkio.Bearer_token)

    # 取得したい件数 = RTする件数
    counts = 35

    # リストのツイート取得 非公開リストは取得NG 公開設定にする
    response = client.get_list_tweets(id=1514978714572173313, max_results=counts, expansions=["attachments.media_keys"])
    tweet = response.data
    random.shuffle(tweet)
    print(tweet)

    for media in tweet:
        mediatw = media.data
        if 'attachments' in mediatw: #動画つきのツイートだけに絞り込む
            post = media.id # 動画つきのツイートのIDだけ抜き出す
            wait = random.uniform(10, 20)
            time.sleep(wait)
            try:
                client.retweet(post) # 自動RT
            except Exception as e:
                print(e)
            else:
                print('RT完了!!')


tweet()
