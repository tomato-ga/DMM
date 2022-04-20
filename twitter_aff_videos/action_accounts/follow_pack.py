import tweepy
import time
import random
from tweepy import TweepyException
import pandas as pd

import api_HjQhq as API
import follow_db



class Get_follower:

    def apicall(self, API):
        client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
            access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)
        return client

    """特定ユーザーからフォロー候補IDを取得"""
    def followers_recently(self, client, username, maxcount) -> list:
        targetid = client.get_user(username=username)
        followers = client.get_users_followers(id=targetid.data.id, max_results=maxcount, user_fields=["id", "name"])
        print(followers, type(followers))

        # フォローするIDをリスト化
        fid =  [follow.id for follow in followers.data]
        print(fid)
        return fid

    """フォロー候補のIDをDBから読み込み"""
    def db_read(self):
        newfollow_db_collection = follow_db.Follow_kouho_db_set()
        return newfollow_db_collection

    """自分アカウントのフォローしてるIDを取得"""
    def followed_mine(self, client): #ids, new_fid
        followed = client.get_users_following(id=1514977383216205834, user_fields=["id", "name"])
        follow_id_list = [follow.id for follow in followed.data]
        # no_follow_id = list(set(fid + new_fid))
        # print(no_follow_id)
        return follow_id_list

    """DBつきあわせて差分取得する"""
    def follow_kouho(self):
        collection = follow_db.Follow_kouho_db_set()
        print('Follow候補数', len(collection))
        my_collction = follow_db.My_following_id_db_set()
        print('フォローしたID数', len(my_collction))
        follow_ids = collection - my_collction #TODO pymongoでDBの差分抽出
        return follow_ids

    """フォロー10人する"""
    def follow10(self,client, no_follow_id):
        no_follow_id = no_follow_id

        count = 0
        while count > 10:
            for fid in no_follow_id:
                client.follow_user(target_user_id=fid)


class Follow_twid(Get_follower):
    def follow_id(self):
        pass

class DB(Get_follower):
    def pas(self):
        pass


i = Get_follower()
client = i.apicall(API)
# new_fid = i.followers_recently(client)
followed_id = i.Followed_mine(client)

# i.Follow10(no_follow_id, client)
