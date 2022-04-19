import tweepy
import api_togsi7
import time
import random


def tweet():

    wait = random.uniform(10, 25)
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_togsi7.API_KEY, consumer_secret=api_togsi7.API_SECRET, access_token=api_togsi7.ACCESS_TOKEN, \
        access_token_secret=api_togsi7.ACCESS_TOKEN_SECRET, bearer_token=api_togsi7.Bearer_token)

    # # リストのツイート取得 非公開リストは取得NG 公開設定にする
    # response = client.get_list_tweets(id=1514978714572173313, max_results=15, expansions=["attachments.media_keys"])
    # tweet = response.data
    # random.shuffle(tweet)
    # print(tweet)

    # """他者アカウント"""
    # rt_count = 0
    # while rt_count == 3:
    #     for media in tweet:
    #         mediatw = media.data
    #         if 'attachments' in mediatw: #動画つきのツイートだけに絞り込む
    #             post = media.id # 動画つきのツイートのIDだけ抜き出す
    #             time.sleep(wait)
    #             try:
    #                 client.retweet(post) # 自動RT
    #                 rt_count += 1
    #             except Exception as e:
    #                 print(e)
    #             else:
    #                 print('RT完了')


    """自分アカウント"""

    ids: list = [
        1514977383216205834,
        1515978583730458630,
        1515697390480945160
    ]

    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=10, exclude='retweets', expansions=["attachments.media_keys"])
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
                    print('自分のRT完了!!')


tweet()

