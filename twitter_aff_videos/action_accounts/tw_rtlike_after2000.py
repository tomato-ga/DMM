import tweepy
import time
import random
import api_after2000
from log_create import getMyLogger


def tweet():

    logger = getMyLogger(__file__)
    logger.debug('デバッグ')

    wait1 = random.random()
    wait2 = random.randint(15, 20)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=api_after2000.API_KEY, consumer_secret=api_after2000.API_SECRET, access_token=api_after2000.ACCESS_TOKEN, access_token_secret=api_after2000.ACCESS_TOKEN_SECRET, bearer_token=api_after2000.Bearer_token)


    for id_mine in api_after2000.ids:
        match id_mine:
            case 1514514623743291395 | 1498937221344563206:

                try:
                    tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
                    print(tweets_get)

                    for t in tweets_get.data:
                            client.like(t.id)
                            print('いいねRT完了')
                            time.sleep(wait)
                except:
                    pass

            case _:
                try:
                    tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
                    print(tweets_get)

                    for t in tweets_get.data:
                            client.like(t.id)
                            client.retweet(t.id)
                            print('いいねRT完了')
                            time.sleep(wait)
                except:
                    pass

tweet()


