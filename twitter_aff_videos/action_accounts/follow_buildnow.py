import tweepy
import time
import random
from tweepy import TweepyException
import pandas as pd

import api_OtxSf as API #TODO テスト中


def APIcall(API):

    client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
        access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)
    return client


def followers_recently():
    client =  APIcall(API)
    followers = client.get_users_followers(id=1515697390480945160, max_results=50, user_fields=["id", "name"])
    print(followers, type(followers))

followers_recently()
