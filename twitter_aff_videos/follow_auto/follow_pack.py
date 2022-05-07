import tweepy
import time
import random
from tweepy import TweepyException

import follow_db



class Get_follower:


    def __init__(self) -> None:
        pass


    def apicall(self, API):
        client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
            access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token)
        return client


    def followers_recently(self, client, username, maxcount) -> list:
        """特定ユーザーからフォロー候補IDを取得"""
        targetid = client.get_user(username=username)
        followers = client.get_users_followers(id=targetid.data.id, max_results=maxcount, user_fields=["id", "name"])
        print(followers, type(followers))

        # フォローするIDをリスト化
        fid =  [follow.id for follow in followers.data]
        print(fid)
        return fid


    def follow_kouho_db_read(self):
        """フォロー候補のIDをDBから読み込み"""
        newfollow_db_collection = follow_db.follow_kouho_db_set()
        return newfollow_db_collection


    def followed_mine(self, client, my_id):
        """自分アカウントのフォローしてるIDを取得"""
        followed = client.get_users_following(id=my_id, user_fields=["id", "name"])
        follow_id_list = [follow.id for follow in followed.data]
        # no_follow_id = list(set(fid + new_fid))
        # print(no_follow_id)
        return follow_id_list


    def follower_mine(self, client, my_id):
        follower = client.get_users_followers(id=my_id, user_fields=["id", "name"])
        follower_id_list = [follower.id for follower in follower.data]
        print(follower, len(follower))
        return follower_id_list



    def follow10(self,client, no_follow_id):
        """フォロー10人する"""
        no_follow_id = no_follow_id

        count = 0
        for fid in no_follow_id:
            while count < 3:
                try:
                    follow = client.follow_user(target_user_id=fid) #TODO ifもしフォローしてたらスルーする処理を追加
                    time.sleep(60)

                    if follow.data['following'] == True:
                        count += 1
                    elif follow.data['following'] == False:
                        count = count
                    # time.sleep(60)
                    print('フォロー完了しました')
                except Exception as ex:
                    print(ex)
                    pass
                if count == 3:
                    break


    def unfollow(self, client, un_follow_id):
        un_follow_id = un_follow_id

        for fid in un_follow_id:
            try:
                client.unfollow_user(target_user_id=fid)
                time.sleep(60)
            except Exception as ex:
                print('[unfollow] Except : ', ex)
                pass
