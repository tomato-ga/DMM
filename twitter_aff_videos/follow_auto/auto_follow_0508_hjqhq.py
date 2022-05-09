import auto_follow_unfollow_module
import api_OtxSf as API
import os

client = auto_follow_unfollow_module.apicall(API)
my_id = 1515978583730458630 #←たまじろう  # 1515514246775582722 # ←動画かくさん野郎  # togsi ID 1515696887781015558
name = 'OtxSf'
get_dir = os.getcwd()


### 最新のJSONにする
auto_follow_unfollow_module.following_json_save(client=client, my_id=my_id, name=name)
auto_follow_unfollow_module.new_follow_json_save(client=client, name=name)

### フォロー実施 ###
follow_list = auto_follow_unfollow_module.new_follow_id_only(name=name)
follow_done_list = auto_follow_unfollow_module.follows(client, follow_list)

### フォローしたらJSONへ保存する
if follow_done_list:
    for i in follow_done_list:
        follow_list.append(i)

    following_list = list(set(follow_list)) #setはJSON保存できないのでリストにする
    new_following = {}
    new_following['id'] = following_list
    auto_follow_unfollow_module.json_save(ids=new_following, json_name=f'{name}_following_id')