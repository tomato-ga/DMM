import tweepy
import api_HjQhq
import time
import random


def tweet():

    wait = random.uniform(10, 25)
    wait_long = random.uniform(30, 50)

    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_HjQhq.API_KEY, consumer_secret=api_HjQhq.API_SECRET, access_token=api_HjQhq.ACCESS_TOKEN, \
        access_token_secret=api_HjQhq.ACCESS_TOKEN_SECRET, bearer_token=api_HjQhq.Bearer_token)

    """自分アカウント"""

    ids: list = [
        1515696887781015558,
        1514977383216205834,
        1515978583730458630,
        1515697390480945160
    ]

    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=5, exclude='retweets', expansions=["attachments.media_keys"])
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
                    time.sleep(wait_long)
                except Exception as e:
                    print(e)
                else:
                    print('自分のRT完了!!')


tweet()

