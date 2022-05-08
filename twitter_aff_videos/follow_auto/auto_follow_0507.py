import api_togsi7 as API
import tweepy
import random
import time

client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
            access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)

response = client.get_list_tweets(id=1514978714572173313, max_results=50,  expansions=["attachments.media_keys","referenced_tweets.id"])
tweets = response.data
random.shuffle(tweets)


like_user_follow = 0
for tweet in tweets:
    tid = tweet.id
    like_users = client.get_liking_users(tid)
    follows = like_users.data
    if follows:
        print('follows（フォローする人）がいました')
        match follows:
            case follows if len(follows) > 0 :
                for follow in follows:
                    follow_response = client.follow_user(target_user_id=follow.id)
                    like_user_follow += 1
                    print(f'フォロー完了: {like_user_follow}人フォローしました')
                    time.sleep(60)
                    if like_user_follow >= 40:
                        break

            case _:
                print('Exception')
                raise Exception('error dasu')



# TODO DBかjsonと連携させる
