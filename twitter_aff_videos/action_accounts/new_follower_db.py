import follow_pack
import pymongo


"""フォロー候補IDを格納するDB読み込み"""
def Follow_kouho_db_set():
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.newfollow

    return collection


"""フォロー候補のIDをDBに保存する"""
def Follow_kouho_id_save_db(new_follower: list):
    collection = Follow_kouho_db_set()
    collection.insert_one(new_follower)


"""自分のフォローIDのDB読み込み"""
def db_set_my_following_id():
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.myfollow

    return collection


"""自分のフォローIDのDBに保存する"""
def following_id_save_db():
    collection = db_set_my_following_id()
