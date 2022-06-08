import tweepy
import time
import random
import api_togsi7


def tweet():

    wait1 = random.random()
    wait2 = random.randint(40, 60)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=api_togsi7.API_KEY, consumer_secret=api_togsi7.API_SECRET, access_token=api_togsi7.ACCESS_TOKEN, access_token_secret=api_togsi7.ACCESS_TOKEN_SECRET, bearer_token=api_togsi7.Bearer_token)


    for id_mine in api_togsi7.ids:
        match id_mine:
            case 1514514623743291395:

                tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
                print(tweets_get)

                for t in tweets_get.data:
                    try:
                        client.like(t.id)
                        time.sleep(wait)
                    except:
                        pass

                print('いいねRT完了')

            case _:
                tweets_get = client.get_users_tweets(id=id_mine, exclude=['retweets', 'replies'], max_results=20, expansions=["attachments.media_keys"])
                print(tweets_get)

                for t in tweets_get.data:
                    try:
                        client.like(t.id)
                        client.retweet(t.id)
                        time.sleep(wait)
                    except:
                        pass

                print('いいねRT完了')


tweet()


