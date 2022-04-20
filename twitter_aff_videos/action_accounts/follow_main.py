import pymongo
import follow_pack
import follow_db

import api_HjQhq as API






pack = follow_pack.Get_follower()
client = pack.apicall(API=API)


"""新しいフォロワーをDBに保存する"""
def new_follows_in_db():
    follow_ids = pack.followers_recently(client=client, username='echi2tube', maxcount=1000)
    for follow_id in follow_ids:
        follow_db.follow_kouho_id_save_db(dict(id=follow_id))

# new_follows_in_db()


def my_follow_in_db():
    my_followed_id = pack.followed_mine(client=client, my_id=1514977383216205834)

    for my_follow in my_followed_id:
        follow_db.my_following_id_save_db(dict(id=my_follow))


# my_follow_in_db()


