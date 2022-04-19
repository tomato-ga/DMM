import tweepy
import api_1j_mc
import time
import random


wait = random.uniform(10, 25)
wait_long = random.uniform(30, 50)


def My_rt():

    """自分アカウントの公式リツイートだけ"""

    client = tweepy.Client(consumer_key=api_1j_mc.API_KEY, consumer_secret=api_1j_mc.API_SECRET, access_token=api_1j_mc.ACCESS_TOKEN, \
        access_token_secret=api_1j_mc.ACCESS_TOKEN_SECRET, bearer_token=api_1j_mc.Bearer_token)

    """自分アカウント"""

    ids: list = [
        1515696887781015558, # togsi
        1514977383216205834, # tomorrow
        1515978583730458630 # OtxSf
    ]


    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=5, exclude='retweets', expansions=["attachments.media_keys","author_id","referenced_tweets.id"], tweet_fields=["context_annotations","created_at","text","source","entities"])
            name: list = [username_0.data['username'] for username_0 in timeline.includes['users']]
            username =name[0]

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
                    ref_tweet = client.create_tweet(text=f'https://twitter.com/{username}/status/{post_mine}/video/1')
                    time.sleep(wait_long)
                    reply_id =  ref_tweet[0]['id']
                    expand_url = [x['expanded_url'] for x in rttw['entities']['urls']]
                    af_url = expand_url[0]

                    if 'dmm' in af_url or 'mgs' in af_url:
                        client.create_tweet(in_reply_to_tweet_id=reply_id, text=f'作品はこちら{af_url}')
                        time.sleep(wait_long)
                except Exception as e:
                    print(e)
                else:
                    print('自分のRTとReply完了!!')


My_rt()
