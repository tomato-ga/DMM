from follow_pack import Get_follower
import follow_main
import follow_parse
import random

import api_OtxSf as API

pack = Get_follower()
client = pack.apicall(API=API)

"""フォローIDを再取得する→
差分取得→フォロー実施""" #TODO フォローするのを自動化する
follow_main.my_follow_in_db(client) #フォローIDを再取得する
follow_suru_ids, follow_kaijo_ids = follow_parse.follow_parse()
random.shuffle(follow_suru_ids)


"""フォロー実施"""
pack.follow10(client, follow_suru_ids)
