import tweepy
import api_togsi7 as API
import json
import ujson
import random
import time
import logging


logger = logging.getLogger("tweepy")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="tweepy.log")
logger.addHandler(handler)

def apicall(API):
    client = tweepy.Client(consumer_key=API.API_KEY, consumer_secret=API.API_SECRET, access_token=API.ACCESS_TOKEN, \
        access_token_secret=API.ACCESS_TOKEN_SECRET, bearer_token=API.Bearer_token, wait_on_rate_limit=True)
    return client

def followed_mine(client, my_id):
    """自分アカウントのフォローしてるIDを取得"""
    followed = client.get_users_following(id=my_id, user_fields=["id", "name"])
    follow_id_list = [follow.id for follow in followed.data]
    # no_follow_id = list(set(fid + new_fid))
    # print(no_follow_id)
    print(follow_id_list)
    print(len(follow_id_list))

    follow_dict: dict[str] = {'id': follow_id_list}
    print(follow_dict)
    return follow_dict


def json_save(ids: dict[str], json_name: str) -> json:
    """_summary_
    フォロー or フォロワー候補IDをjson dump
    Args:
        ids (dict[str]): フォロー or フォロワー候補のIDをdict ['id]で渡す
        json_name (_type_): strで渡すとファイル名に使われる
    """
    with open(f'./{json_name}.json', 'w', encoding='utf-8') as f:
        json.dump(ids, f, indent=4, ensure_ascii=False)


def new_follow_id(client) -> dict[str]:
    """_summary_
    最新のツイートにいいねしているアカウントIDを取得する

    Args:
        client (_type_): tweepyインスタンスを渡す

    Returns:
        dict[str]: 新しくフォローするアカウントIDをdictで返す
    """

    response = client.get_list_tweets(id=1514978714572173313, max_results=15,  expansions=["attachments.media_keys","referenced_tweets.id"])
    tweets = response.data
    random.shuffle(tweets)

    follow_id_lists = []
    max_count= 40

    for tweet in tweets:
        tid = tweet.id
        like_users = client.get_liking_users(tid) # TODO マックス40人までとかに制限する
        follows = like_users.data

        if follows:
            print(f'follows（フォローする人）が{len(like_users)}人いました')

            for follow in follows:
                follow_id_lists.append(follow.id)

    new_follow_dict: dict[str] = {'id': follow_id_lists[:max_count]}
    print(len(follow_id_lists), follow_id_lists[:max_count])
    return new_follow_dict


def follows(client, follow_list: list):
    """_summary_
    フォロー実施関数
    最大40人まで

    Args:
        client (instance):  tweepyインスタンスを渡す
        follow_list (list): 新しくフォローするIDだけ抽出したリストを渡す
    """
    like_user_follow = 0

    for id in follow_list:
        client.follow_user(target_user_id=id)
        print('フォローしました')
        like_user_follow += 1
        print(f'フォロー完了: {like_user_follow}人フォローしました')
        time.sleep(60)
        if like_user_follow >= 40:
            break


### フォローしてる人をJSON保存
my_id = 1515696887781015558 #togsi ID
client = apicall(API)
follow_dict = followed_mine(client, my_id)
json_save(ids=follow_dict, json_name='following_id')


### 新しくフォローする人をJSON保存
client = apicall(API)
new_follow_dict = new_follow_id(client)
json_save(new_follow_dict, json_name='new_follow_id')


### フォローしてる人のJSONを読み込む
following: json = ujson.load(open('following_id.json'))
following_list = following['id']
len(following['id'])

### フォローする人のJSONを読み込む
new_follow: json = ujson.load(open('./new_follow_id.json'))
new_follow_list = new_follow['id']
len(new_follow_list)


### 新しくフォローするIDだけ抽出
follow_list = list(set(new_follow_list)- set(following_list))
len(follow_list)


### フォローしたらJSONへ保存する
for i in follow_list:
    following_list.append(i)

following_list = list(set(following_list)) #setはJSON保存できないのでリストにする
new_following = {}
new_following['id'] = following_list
json_save(ids=new_following, json_name='following_id')