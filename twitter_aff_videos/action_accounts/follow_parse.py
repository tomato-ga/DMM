import pandas as pd
import pprint

import follow_pack
import follow_db

import api_HjQhq as API


pack = follow_pack.Get_follower()


"""フォローしてないID取得のため、差分取得"""
def follow_parse():
    kouho_id =follow_db.follow_kouho_db_set()
    following_id = follow_db.my_following_id_db_set()

    kouho_df = pd.DataFrame(kouho_id.find())
    following_df = pd.DataFrame(following_id.find())

    kouho_list = kouho_df['id'].values.tolist()
    following_list = following_df['id'].values.tolist()

    follow_suru_ids = list(set(kouho_list + following_list))
    print(follow_suru_ids, len(follow_suru_ids))
    return follow_suru_ids


follow_suru_ids = follow_parse()
client = pack.apicall(API=API)
pack.follow10(client, follow_suru_ids)
