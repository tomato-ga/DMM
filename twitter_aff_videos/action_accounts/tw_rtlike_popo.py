import tweepy
import time
import random
import api_popo5ppo


def tweet():

    wait1 = random.random()
    wait2 = random.randint(25, 30)
    wait = round(wait1 + wait2,3)


    client = tweepy.Client(consumer_key=api_popo5ppo.API_KEY, consumer_secret=api_popo5ppo.API_SECRET, access_token=api_popo5ppo.ACCESS_TOKEN, access_token_secret=api_popo5ppo.ACCESS_TOKEN_SECRET, bearer_token=api_popo5ppo.Bearer_token)


    for id_mine in api_popo5ppo.ids:
        match id_mine:
            case 1514514623743291395 | 1498937221344563206:

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


