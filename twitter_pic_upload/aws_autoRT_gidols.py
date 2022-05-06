import tweepy
import api_gidolsa
import time
import random

def tweet(event, context): # event, context
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_gidolsa.API_KEY, consumer_secret=api_gidolsa.API_SECRET, access_token=api_gidolsa.ACCESS_TOKEN, access_token_secret=api_gidolsa.ACCESS_TOKEN_SECRET, bearer_token=api_gidolsa.Bearer_token)

    # 取得したい件数 = RTする件数
    counts = 30

    #ランダム待機時間
    wait = random.uniform(10, 20)
    wait1 = random.random()
    wait2 = random.randint(30,50)
    wait_like = round(wait1 + wait2,3)

    # リストのツイート取得 非公開リストは取得NG 公開設定にする


    # 素敵なグラビアアイドル様
    response_gidolsa = client.get_list_tweets(id=1521876334074818560, max_results=counts,expansions=["attachments.media_keys"])

    tweet = response_gidolsa.data
    random.shuffle(tweet)
    print(tweet)


    for media in tweet:
        mediatw = media.data
        if 'attachments' in mediatw: #写真つきのツイートだけに絞り込む
            post = media.id # 写真つきのツイートのIDだけ抜き出す
            try:
                client.retweet(post) # 自動RT
                time.sleep(wait)

                print('RT完了!!')
            except Exception as e:
                print(e)
