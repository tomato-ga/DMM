import auto_follow_unfollow_module
import api_togsi7 as API
import os

client = auto_follow_unfollow_module.apicall(API)
my_id = 1515696887781015558
name = 'togsi'
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
    auto_follow_unfollow_module.json_save(ids=new_unfollowing, json_name=f'{name}_unfollow_done_id')
