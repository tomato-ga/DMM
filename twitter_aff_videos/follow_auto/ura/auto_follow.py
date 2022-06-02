import auto_follow_unfollow_module
import os
import API_config_aya
import API_config_yukarin


"""
my_idとnameにアカウントIDと名前を入れる
"""


max_count = 2
get_dir = os.getcwd()
print(get_dir)

id_name_listdict = [
    {
        'my_id': 1522927470231670784,
        'name': 'kclw_d',
        },
    {
        'my_id': 1530817733243588608,
        'name': 'yukarin_sef',
        }
    ]


for ids, APIs in zip(id_name_listdict, [API_config_aya, API_config_yukarin]):
    print(ids['my_id'])
    print(ids['name'])
    print(APIs)


    client = auto_follow_unfollow_module.apicall(APIs)

    ### 最新のJSONにする
    follow_dict = auto_follow_unfollow_module.following_json_save(client=client, my_id=ids['my_id'], name=ids['name'])
    auto_follow_unfollow_module.new_follow_json_save(client=client, name=ids['name'])

    ### フォロー実施 ###
    follow_list = auto_follow_unfollow_module.new_follow_id_only(name=ids['name'])
    follow_done_list = auto_follow_unfollow_module.follows(client, follow_list, max_count)

    ### フォローしたらJSONへ保存する
    if follow_done_list:
        for i in follow_done_list:
            follow_dict['id'].append(i)

            # following_list = list(set(follow_list)) #setはJSON保存できないのでリストにする
            auto_follow_unfollow_module.json_save(ids=follow_dict, json_name=f'/home/don/py/DMM/twitter_aff_videos/follow_auto/ura/{ids["name"]}_following_id')
