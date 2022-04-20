from typing import Collection
import follow_pack
import pymongo

"""新しいフォロワーをDBに保存する"""

def db_set():
    db_url = 'mongodb://pyton:radioipad1215@192.168.0.23:27017'
    client = pymongo.MongoClient(db_url)
    db = client.twitter
    collection = db.newfollower

    return collection


def follower_save(new_follower: list):
    collection = db_set()
    collection.insert_one(new_follower)

