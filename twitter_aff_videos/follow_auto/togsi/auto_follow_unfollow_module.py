import tweepy
import json
import ujson
import random
import time
import logging


# logger = logging.getLogger("tweepy")
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename="tweepy.log")
# logger.addHandler(handler)


"""
想定する流れ

【auto_follow.py】
1. 他人のツイートにいいねしているIDをリスト化
2. フォローしてるIDをリスト化
3. 新しくフォローするIDを抽出: 2-1（フォローしたことないID）のリストを作る
4. 3のリストをフォロー実施
5. フォロー実施したIDをJSONで保存しておく

【auto_unfollow.py】
6. フォローしているIDをリスト化
7. フォロワーにいるIDをリスト化
8. 一方的にフォローしているIDを抽出: 6-7（フォローだけにいるID）のリストを作る
9. 8のリストをアンフォロー実施
10. アンフォロー実施したIDをJSONで保存しておく

11. 1に戻ってループ

"""


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


def follower_mine(client, my_id):
    """_summary_
    自分アカウントのフォロワーIDを取得する

    Args:
        client (_type_): _description_
        my_id (_type_): _description_
    """

    follower = client.get_users_followers(id=my_id, user_fields=["id", "name"])
    follower_id_list = [follower.id for follower in follower.data]
    print(follower_id_list)
    print(len(follower_id_list))

    follower_dict: dict[str] = {'id': follower_id_list}
    print(follower_dict)
    return follower_dict


def json_save(ids: dict[str], json_name: str) -> json:
    """_summary_
    フォロー or フォロワー候補IDをjson dump
    Args:
        ids (dict[str]): フォロー or フォロワー候補のIDをdict ['id]で渡す
        json_name (_type_): strで渡すとファイル名に使われる
    """
    with open(f'./{json_name}.json', 'w+', encoding='utf-8') as f:
        json.dump(ids, f, indent=4, ensure_ascii=False)

    # Mac用ディレクトリ /Users/ore/Documents/GitHub/DMM/twitter_aff_videos/follow_auto/

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
        like_users = client.get_liking_users(tid)
        follows = like_users.data

        if follows:
            for follow in follows:
                follow_id_lists.append(follow.id)

    new_follow_dict: dict[str] = {'id': follow_id_lists[:max_count]}
    print(len(follow_id_lists), follow_id_lists[:max_count])
    print(f'follows（フォローする人）が{len(follow_id_lists)}人いました')
    return new_follow_dict


def follows(client, follow_list: list, max_count) -> list:
    """_summary_
    フォロー実施関数
    最大40人まで

    Args:
        client (instance):  tweepyインスタンスを渡す
        follow_list (list): 新しくフォローするIDだけ抽出したリストを渡す

    return:
        フォローしたIDのリスト
    """
    like_user_follow = 0
    follow_done_list = []

    for id in follow_list:
        follow_response = client.follow_user(target_user_id=id)
        print('フォローしました')
        if follow_response.data['following'] == True:
            like_user_follow += 1
            print(f'フォロー完了: {like_user_follow}人フォローしました')
            follow_done_list.append(id)
        elif follow_response.data['following'] == False:
            like_user_follow = like_user_follow

        time.sleep(100)
        if like_user_follow >= max_count:
            break

    return follow_done_list



def unfollows(client, unfollow_list: list, max_count) -> list:
    """_summary_
    アンフォロー実施関数
    最大40人まで

    Args:
        client (_type_): tweepyインスタンス
        unfollow_list (list): アンフォローするIDのリスト

    Returns:
        list: アンフォローしたIDのリスト
    """

    unfollow_user = 0
    unfollow_done_list = []

    for id in unfollow_list:
        unfollow_response = client.unfollow_user(target_user_id=id)
        print('アンフォローしました')
        if unfollow_response.data['following'] == False:
            unfollow_user += 1
            print(f'アンフォロー完了:{unfollow_user}人アンフォローしました')
            unfollow_done_list.append(id)
        elif unfollow_response.data['following'] == True:
            unfollow_user = unfollow_user

        time.sleep(100)
        if unfollow_user >= max_count:
            break

    return unfollow_done_list



############################実行#####################################

def following_json_save(client, my_id, name):
    """フォローしてる人をJSON保存"""
    my_id = my_id #togsi ID
    follow_dict = followed_mine(client, my_id)
    json_save(ids=follow_dict, json_name=f'./{name}_following_id')
    return follow_dict

def new_follow_json_save(client, name):
    """新しくフォローする人をJSON保存"""
    new_follow_dict = new_follow_id(client)
    json_save(new_follow_dict, json_name=f'./{name}_new_follow_id')


def new_follow_id_only(name) -> list:
    """_summary_
    JSONを読み込んで新しくフォローする人だけのIDを作る

    Returns:
        list: 新しくフォローするIDのリスト
    """
    ### following フォローしてる人のJSONを読み込む
    following: json = ujson.load(open(f'./{name}_following_id.json'))
    following_list = following['id']
    print(f"JSONに保存されているフォローした人は{len(following_list)}人います")

    ### new_follow_id フォローする人のJSONを読み込む
    new_follow = ujson.load(open(f'./{name}_new_follow_id.json'))
    new_follow_list = new_follow['id']

    ### 新しくフォローするIDだけ抽出
    follow_list = list(set(new_follow_list)- set(following_list))
    print(f'新しくフォローする人は{len(follow_list)}人います')
    return follow_list


def follower_json_save(client, my_id, name):
    """フォロワーをJSON保存"""
    my_id = my_id #togsi ID
    follower_dict = follower_mine(client, my_id)
    json_save(ids=follower_dict, json_name=f'{name}_follower_id')
    return follower_dict

def unfollow_id_only(name) -> list:
    """_summary_
    JSONを読み込んでアンフォローする人だけのIDを作る

    Returns:
        list: アンフォローするIDのリスト
    """
    ### following フォローしてる人のJSONを読み込む
    following = ujson.load(open(f'./{name}_following_id.json'))
    following_list = following['id']
    print(f"JSONに保存されているフォローした人は{len(following_list)}人います")

    ### follower フォロワーのJSONを読み込む
    follower = ujson.load(open(f'./{name}_follower_id.json'))
    follower_list = follower['id']

    ### アンフォローするID（一方的にフォローしているID）だけ抽出
    unfollow_list = list(set(following_list) - set(follower_list))
    print(f'新しくアンフォロー（フォロー解除）する人は{len(unfollow_list)}人います')
    return unfollow_list


"""
更新履歴

更新履歴
2022/05/15 16:01
JSON保存場所がMacのディレクトリだったため、CRONが動いていなかった
Macのディレクトリを削除

2022/05/15 16:37

フォロワーリスト引くフォローリストになっていたことで、アンフォローがされていなかった
unfollow_list = list(set(follower_list) - set(following_list))
↓
unfollow_list = list(set(following_list) - set(follower_list))

"""