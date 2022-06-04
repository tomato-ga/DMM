import auto_follow_unfollow_module
import api_1j_mc as API
import os

"""
my_idとnameにアカウントIDと名前を入れる
"""

client = auto_follow_unfollow_module.apicall(API)
my_id = 1515514246775582722
name = 'HjQhq'
max_count = 30
get_dir = os.getcwd()
print(get_dir)

### 最新のJSONにする
follower_dict = auto_follow_unfollow_module.follower_json_save(client=client, my_id=my_id, name=name)
unfollow_list = auto_follow_unfollow_module.unfollow_id_only(name=name)

### アンフォロー実施 ###
unfollow_done_list = auto_follow_unfollow_module.unfollows(client=client, unfollow_list=unfollow_list, max_count=max_count)

### アンフォローしたらJSONへ保存する
unfollow_done = []
if unfollow_done_list:
    for i in unfollow_done_list:
        unfollow_done.append(i)

    unfollowing_list = list(set(unfollow_list)) #setはJSON保存できないのでリストにする
    new_unfollowing = {}
    new_unfollowing['id'] = unfollow_done
    auto_follow_unfollow_module.json_save(ids=new_unfollowing, json_name=f'/home/don/py/DMM/twitter_aff_videos/follow_auto/{name}/{name}_unfollow_done_id')
