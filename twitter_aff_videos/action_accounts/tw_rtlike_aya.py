import tweepy
import time
import random
import API_config_aya


def tweet():

    wait1 = random.random()
    wait2 = random.randint(15, 20)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=API_config_aya.API_KEY, consumer_secret=API_config_aya.API_SECRET, access_token=API_config_aya.ACCESS_TOKEN, access_token_secret=API_config_aya.ACCESS_TOKEN_SECRET, bearer_token=API_config_aya.Bearer_token)


    for id_mine in API_config_aya.ids:

        tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
        print(tweets_get)

        for t in tweets_get.data:
            try:
                client.like(t.id)
                time.sleep(wait)
            except:
                pass

        print('いいね完了')


tweet()


