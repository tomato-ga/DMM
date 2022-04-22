import tweepy
import time
import random

wait = random.uniform(10, 25)
wait_long = random.uniform(30, 50)


def Thirdparty_rt(API):
    """他者アカウント"""

    print('[Thirdparty_rt]: 他人のアカウントのRTスタート')


    # Twitter API v2対応
    client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
        access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)

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


def My_rt(API, ids):
    """自分アカウント"""

    print('[My_rt]: 自分のアカウントのRTスタート')

    client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
        access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)

    """もしAPIキーがこれだったらidを選んでidをforで回すという処理にしたい"""


    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=5, exclude='retweets', expansions=["attachments.media_keys","author_id","referenced_tweets.id"]) # context_annotations削除 tweet_fields=["text","source","entities"]
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
                    print('[My_rt]: 自分のRTとReply完了!!')


def My_new_rt(API, ids):
    """自分アカウントの新規動画投稿RT"""

    client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
        access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)

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
                    ref_tweet = client.create_tweet(text=f'https://twitter.com/{username}/status/{post_mine}/video/1')
                    time.sleep(wait_long)
                    reply_id =  ref_tweet[0]['id']
                    expand_url = [x['expanded_url'] for x in rttw['entities']['urls']]
                    af_url = expand_url[0]

                    if 'dmm' in af_url or 'mgs' in af_url:
                        client.create_tweet(in_reply_to_tweet_id=reply_id, text=f'作品はこちら{af_url}')
                        time.sleep(wait_long)
                except Exception as e:
                    print(e)
                else:
                    print('[My_new_rt]: 自分の新規動画RTとReply完了!!')
