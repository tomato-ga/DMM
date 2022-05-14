import auto_follow_unfollow_module
import api_togsi7 as API

client = auto_follow_unfollow_module.apicall(API)
my_id = 1515514246775582722 # ←動画かくさん野郎
name = 'HjQhq'

### 最新のJSONにする
auto_follow_unfollow_module.follower_json_save(client=client, my_id=my_id, name=name)
unfollow_list = auto_follow_unfollow_module.unfollow_id_only(name=name)

### アンフォロー実施 ###
unfollow_done_list = auto_follow_unfollow_module.unfollows(client=client, unfollow_list=unfollow_list)


### アンフォローしたらJSONへ保存する
if unfollow_done_list:
    for i in unfollow_done_list:
        unfollow_list.append(i)

    unfollowing_list = list(set(unfollow_list)) #setはJSON保存できないのでリストにする
    new_unfollowing = {}
    new_unfollowing['id'] = unfollowing_list
    auto_follow_unfollow_module.json_save(ids=new_unfollowing, json_name=f'{name}_following_id')
