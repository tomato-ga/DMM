import tweepy
import time
import random
import api_tomorrow_genkio


def tweet():

    wait1 = random.random()
    wait2 = random.randint(15, 20)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=api_tomorrow_genkio.API_KEY, consumer_secret=api_tomorrow_genkio.API_SECRET, access_token=api_tomorrow_genkio.ACCESS_TOKEN, access_token_secret=api_tomorrow_genkio.ACCESS_TOKEN_SECRET, bearer_token=api_tomorrow_genkio.Bearer_token)


    for id_mine in api_tomorrow_genkio.ids:

        try:
            tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
            print(tweets_get)

            for t in tweets_get.data:
                    client.like(t.id)
                    print('いいね完了')
                    # いいねだけにしている RTはしてない
                    time.sleep(wait)
        except:
            pass


tweet()
