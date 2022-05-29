import auto_follow_unfollow_module
import api_HjQhq as API
import os


"""
my_idとnameにアカウントIDと名前を入れる
"""

client = auto_follow_unfollow_module.apicall(API)
my_id = 1515514246775582722
name = 'HjQhq'
max_count = 15
get_dir = os.getcwd()
print(get_dir)

### 最新のJSONにする
follow_dict = auto_follow_unfollow_module.following_json_save(client=client, my_id=my_id, name=name)
auto_follow_unfollow_module.new_follow_json_save(client=client, name=name)

### フォロー実施 ###
follow_list = auto_follow_unfollow_module.new_follow_id_only(name=name)
follow_done_list = auto_follow_unfollow_module.follows(client, follow_list, max_count)

### フォローしたらJSONへ保存する
if follow_done_list:
    for i in follow_done_list:
        follow_dict['id'].append(i)

        # following_list = list(set(follow_list)) #setはJSON保存できないのでリストにする
        auto_follow_unfollow_module.json_save(ids=follow_dict, json_name=f'{name}_following_id')
