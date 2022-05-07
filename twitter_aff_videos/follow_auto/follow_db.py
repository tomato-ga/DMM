import pymongo


def follow_kouho_db_set():
    """フォロー候補IDを格納するDB読み込み"""
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.newfollowtomorrow
    return collection


def follow_kouho_id_save_db(new_follower: list):
    """フォロー候補のIDをDBに保存する"""
    collection = follow_kouho_db_set()
    collection.insert_one(new_follower)
    print('DBにフォロー候補のIDを保存しました')


def my_following_id_db_set():
    """自分のフォローIDのDB読み込み"""
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.myfollowtomorrow
    return collection


def my_following_id_save_db(my_following_ids: list):
    """自分のフォローIDのDBに保存する"""
    collection = my_following_id_db_set()
    collection.insert_one(my_following_ids)
    print('自分がフォローしているIDをDBに保存しました')


def my_follower_id_db_set():
    """自分のフォロワーIDのDB読み込み"""
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.myfollowertomorrow
    return collection


def my_follower_id_save_db(my_follower_ids: list):
    """自分のフォローIDのDBに保存する"""
    collection = my_follower_id_db_set()
    collection.insert_one(my_follower_ids)
    print('自分のフォロワーIDをDBに保存しました')
