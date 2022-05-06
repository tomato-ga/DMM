import tweepy
import api_gidolsa
import random
import time

def like():
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_gidolsa.API_KEY, consumer_secret=api_gidolsa.API_SECRET, access_token=api_gidolsa.ACCESS_TOKEN, access_token_secret=api_gidolsa.ACCESS_TOKEN_SECRET, bearer_token=api_gidolsa.Bearer_token)

    # 取得したい件数 = RTする件数
    counts = 10

    #ランダム待機時間
    wait1 = random.random()
    wait2 = random.randint(100,150)
    wait = round(wait1 + wait2,3)

    # リストのツイート取得 非公開リストは取得NG 公開設定にする
    # にゃごのリスト
    response = client.search_recent_tweets(query='#グラビア has:media', max_results=counts,expansions=["attachments.media_keys"]) #tweet_fields=['created_at'],
    tweet = response.data
    random.shuffle(tweet)

    for media in tweet:
        mediatw = media.data
        if 'attachments' in mediatw: #写真つきのツイートだけに絞り込む
            post = media.id # 写真つきのツイートのIDだけ抜き出す
            wait = random.uniform(10, 20)
            time.sleep(wait)
            try:
                client.like(post) # 自動いいね
            except Exception as e:
                print(e)
            else:
                print('いいね完了!!')

like()