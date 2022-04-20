import tweepy
import time
import random
from tweepy import TweepyException
import pandas as pd

import api_HjQhq as API
import new_follower_db


class Get_follower:

    """APIの準備"""
    def APIcall(self, API):
        client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
            access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)
        return client


    """特定ユーザーからフォロー候補IDを取得"""
    def Followers_recently(self, client, username, maxcount) -> list:
        targetid = client.get_user(username=username)
        followers = client.get_users_followers(id=targetid.data.id, max_results=maxcount, user_fields=["id", "name"])
        print(followers, type(followers))

        # フォローするIDをリスト化
        fid =  [follow.id for follow in followers.data]
        print(fid)
        return fid


    """フォロー候補のIDをDBから読み込み"""
    def Db_read(self):
        newfollow_db_collection = new_follower_db.Follow_kouho_db_set()
        return newfollow_db_collection


    """自分アカウントのフォローしてるIDを取得"""
    def Followed_mine(self, client): #ids, new_fid
        followed = client.get_users_following(id=1514977383216205834, user_fields=["id", "name"])
        follow_id_list = [follow.id for follow in followed.data]
        # no_follow_id = list(set(fid + new_fid))
        # print(no_follow_id)
        return follow_id_list


    """DBつきあわせて差分取得する"""
    def Follow_kouho(self):
        print('Follow候補数', len())


    """フォロー10人する"""
    def Follow10(self,client, no_follow_id):
        no_follow_id = no_follow_id

        count = 0
        while count > 10:
            for fid in no_follow_id:
                client.follow_user(target_user_id=fid)


i = Get_follower()
client = i.APIcall(API)
# new_fid = i.followers_recently(client)
followed_id = i.Followed_mine(client)

# i.Follow10(no_follow_id, client)
