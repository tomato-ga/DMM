import follow_pack
import follow_db
import follow_parse
import random

import api_HjQhq as API



pack = follow_pack.Get_follower()
client = pack.apicall(API=API)


"""新しいフォロー候補IDをDBに保存する
usernameを変えるとフォロー候補を取得可能 maxcountは取得件数
"""
def new_follows_in_db():
    follow_ids = pack.followers_recently(client=client, username='echi2tube', maxcount=1000)
    for follow_id in follow_ids:
        follow_db.follow_kouho_id_save_db(dict(id=follow_id))

# new_follows_in_db()

"""自分がフォローしているIDをDBに保存する"""
def my_follow_in_db():
    my_followed_id: list = pack.followed_mine(client=client, my_id=1514977383216205834)

    for my_follow in my_followed_id:
        follow_db.my_following_id_save_db(dict(id=my_follow))


# my_follow_in_db()


"""自分のフォロワーIDをDBに保存する"""
def my_follower_in_db():
    my_follower_id: list = pack.follower_mine(client, my_id=1514977383216205834)

    for my_follower in my_follower_id:
        follow_db.my_follower_id_save_db(dict(id=my_follower))

# my_follower_in_db()

#################################################

# pack = follow_pack.Get_follower()
# client = pack.apicall(API=API)

# """フォローIDを再取得する→
# 差分取得→フォロー実施""" #TODO フォローするのを自動化する
# follow_main.my_follow_in_db() #フォローIDを再取得する
# follow_suru_ids, follow_kaijo_ids = follow_parse.follow_parse()
# random.shuffle(follow_suru_ids)


# """フォロー実施"""
# pack.follow10(client, follow_suru_ids)


"""フォロー解除実施"""
# pack.unfollow(client, follow_kaijo_ids)
