import pandas as pd
import pprint
import random

import follow_pack
import follow_db
import follow_main

import api_tomorrow_genkio as API


pack = follow_pack.Get_follower()


"""フォローしてないID取得のため、差分取得=tweepyでフォローするIDの取得"""
def follow_parse() -> list:
    kouho_id =follow_db.follow_kouho_db_set()
    following_id = follow_db.my_following_id_db_set()

    kouho_df = pd.DataFrame(kouho_id.find())
    following_df = pd.DataFrame(following_id.find())

    kouho_list = kouho_df['id'].values.tolist()
    following_list = following_df['id'].values.tolist()

    follow_suru_ids = list(set(kouho_list) - set(following_list))
    print(follow_suru_ids, len(follow_suru_ids))
    return follow_suru_ids


"""フォローIDを再取得する→
差分取得→フォロー実施""" #TODO フォローするのを自動化する
follow_main.my_follow_in_db()
follow_suru_ids = follow_parse()
random.shuffle(follow_suru_ids)

client = pack.apicall(API=API)
pack.follow10(client, follow_suru_ids)
