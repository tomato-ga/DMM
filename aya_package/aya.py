import tweepy
import API_config_aya
import json
import random


def tweet():

    client = tweepy.Client(consumer_key=API_config_aya.API_KEY, consumer_secret=API_config_aya.API_SECRET, access_token=API_config_aya.ACCESS_TOKEN, access_token_secret=API_config_aya.ACCESS_TOKEN_SECRET, bearer_token=API_config_aya.Bearer_token)

    jk = json.load(open('aya_text.json', 'r'))
    text = jk['tweet']
    t = random.choice(text)
    tweet_text= t['text']

    client.create_tweet(text=tweet_text)
