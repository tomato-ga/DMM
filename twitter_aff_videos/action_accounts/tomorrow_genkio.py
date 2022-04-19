import tweepy
import api_tomorrow_genkio
import time
import random


def tweet():

    wait = random.uniform(10, 25)
    wait_long = random.uniform(30, 50)
    # Twitter API v2対応
    client = tweepy.Client(consumer_key=api_tomorrow_genkio.API_KEY, consumer_secret=api_tomorrow_genkio.API_SECRET, access_token=api_tomorrow_genkio.ACCESS_TOKEN, \
        access_token_secret=api_tomorrow_genkio.ACCESS_TOKEN_SECRET, bearer_token=api_tomorrow_genkio.Bearer_token)

    # リストのツイート取得 非公開リストは取得NG 公開設定にする
    response = client.get_list_tweets(id=1514978714572173313, max_results=15, expansions=["attachments.media_keys"])
    tweet = response.data
    random.shuffle(tweet)
    print(tweet)

    """他者アカウント"""
    rt_count = 0
    while rt_count == 3:
        for media in tweet:
            mediatw = media.data
            if 'attachments' in mediatw: #動画つきのツイートだけに絞り込む
                post = media.id # 動画つきのツイートのIDだけ抜き出す
                time.sleep(wait)
                try:
                    client.retweet(post) # 自動RT
                    rt_count += 1
                except Exception as e:
                    print(e)
                else:
                    print('RT完了')


    """自分アカウント"""

    ids: list = [
        1515696887781015558,
        1515697390480945160,
        1515978583730458630
    ]

    rt_count_mine = 0
    for id_mine in ids:
        try:
            timeline = client.get_users_tweets(id=id_mine, max_results=10, exclude='retweets', expansions=["attachments.media_keys","author_id","referenced_tweets.id"], tweet_fields=["context_annotations","public_metrics","created_at", "text", "source", "geo"])
            name: list = [username_0.data['username'] for username_0 in timeline.includes['users']]
            username =name[0]

            rts_tweet = timeline.data
            random.shuffle(rts_tweet)
            print(rts_tweet)
        except Exception as ex:
            print(ex)
            pass

        while rt_count_mine == 1:
            for rt_tweet in rts_tweet:
                rttw = rt_tweet.data
                if 'attachments' in rttw:
                    post_mine = rt_tweet.id
                    time.sleep(wait)
                    try:
                        ref_tweet = client.create_tweet(text=f'https://twitter.com/{username}/status/{post_mine}/video/1')
                        time.sleep(wait_long)
                        reply_id =  ref_tweet[0]['id']
                        rt_count_mine += 1

                        if rttw['text']:
                            af_url_text_full = rttw['text']
                            af_url_list = af_url_text_full.split(' ')
                            af_url = af_url_list[1]
                            client.create_tweet(in_reply_to_tweet_id=reply_id, text=f'これだな{af_url}')
                            time.sleep(wait_long)
                    except Exception as e:
                        print(e)
                    else:
                        print('自分のRTとReply完了!!')



tweet()

