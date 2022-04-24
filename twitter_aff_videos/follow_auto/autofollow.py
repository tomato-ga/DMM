from follow_pack import Get_follower
import follow_main
import follow_parse
import random

import api_HjQhq as API

pack = Get_follower()
client = pack.apicall(API=API)


###################アカウントで1000人フォローしてたときのスクリプト##########################

"""アカウントのフォロワー（フォローするID）を再取得する→
差分取得→フォロー実施""" #TODO フォローするのを自動化する
# follow_main.my_follow_in_db(client) #フォローIDを再取得する
# follow_suru_ids, follow_kaijo_ids = follow_parse.follow_parse()
# random.shuffle(follow_suru_ids)


"""フォロー実施"""
# pack.follow10(client, follow_suru_ids)

###################アカウントで1000人フォローしてたときのスクリプト##########################


###################リストから最新ツイート取得してLIKEしてるユーザーをフォロー##########################

response = client.get_list_tweets(id=1514978714572173313, max_results=15,  expansions=["attachments.media_keys","author_id","referenced_tweets.id"])
tweets = response.data
random.shuffle(tweets)

like_user_follow = 0

for tweet in tweets:
    while like_user_follow < 2:
        tid = tweet.id
        like_users = client.get_liking_users(tid)
        follows = like_users.data

        if follows:
            for follow in follows:
                client.follow_user(target_user_id=follow.id)
                like_user_follow += 1
                if like_user_follow == 2:
                    break

###################リストから最新ツイート取得してLIKEしてるユーザーをフォロー##########################
