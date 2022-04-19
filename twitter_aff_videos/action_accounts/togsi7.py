import tweepy
import api_togsi7
import time
import random


"""
引用動画にアフィURLをつけてさらに拡散
# author_idを取得してusernameを取得、/video/1をつけてツイートする
アフィURL取得→自分のツイートにアフィURLをつけてreply
"""

def tweet():

    wait = random.uniform(10, 25)
    wait_long = random.uniform(30, 50)
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_togsi7.API_KEY, consumer_secret=api_togsi7.API_SECRET, access_token=api_togsi7.ACCESS_TOKEN, \
        access_token_secret=api_togsi7.ACCESS_TOKEN_SECRET, bearer_token=api_togsi7.Bearer_token)


    """自分アカウント"""

    ids: list = [
        1514977383216205834,
        1515978583730458630,
        1515697390480945160
    ]

    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=1, exclude='retweets', expansions=["attachments.media_keys","author_id","referenced_tweets.id"], tweet_fields=["context_annotations","public_metrics","created_at", "text", "source", "geo"])
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
                    if rttw['text']:
                        af_url_text_full = rttw['text']
                        af_url_list = af_url_text_full.split(' ')
                        af_url = af_url_list[1]
                        client.create_tweet(in_reply_to_tweet_id=reply_id, text=f'特定！{af_url}')
                        time.sleep(wait_long)
                except Exception as e:
                    print(e)
                else:
                    print('自分のRTとReply完了!!')


tweet()
