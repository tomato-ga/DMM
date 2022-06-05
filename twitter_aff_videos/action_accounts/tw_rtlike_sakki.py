import tweepy
import time
import random
import API_config_sakki


def tweet():

    wait1 = random.random()
    wait2 = random.randint(50,400)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=API_config_sakki.API_KEY, consumer_secret=API_config_sakki.API_SECRET, access_token=API_config_sakki.ACCESS_TOKEN, access_token_secret=API_config_sakki.ACCESS_TOKEN_SECRET, bearer_token=API_config_sakki.Bearer_token)


    for id_mine in API_config_sakki.ids:

        tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=5, expansions=["attachments.media_keys"])
        print(tweets_get)

        for t in tweets_get.data:
            try:
                client.like(t.id)
                time.sleep(wait)
            except:
                pass

        print('いいねRT完了')


tweet()


