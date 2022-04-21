import pandas as pd
import follow_db



"""フォローしてないID取得のため、差分取得=tweepyでフォローするIDの取得"""
def follow_parse() -> list:
    kouho_id =follow_db.follow_kouho_db_set() #フォロー候補ID取得
    following_id = follow_db.my_following_id_db_set() #フォローしたID取得
    follower_id = follow_db.my_follower_id_db_set() #フォロワーを取得

    kouho_df = pd.DataFrame(kouho_id.find())
    following_df = pd.DataFrame(following_id.find())
    follower_df = pd.DataFrame(follower_id.find())

    kouho_list = kouho_df['id'].values.tolist()
    following_list = following_df['id'].values.tolist()
    follower_list = follower_df['id'].values.tolist()

    follow_suru_ids = list(set(kouho_list) - set(following_list))
    print(follow_suru_ids, len(follow_suru_ids))

    follow_kaijo_ids = list(set(following_list) - set(follower_list))

    return follow_suru_ids, follow_kaijo_ids
