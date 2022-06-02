import auto_follow_unfollow_module
import os
import api_OtxSf
import api_togsi7
import api_HjQhq
import api_1j_mc

"""
my_idとnameにアカウントIDと名前を入れる
"""

max_count = 35
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


for ids, APIs in zip(id_name_listdict, [api_OtxSf, api_1j_mc, api_HjQhq, api_togsi7]):
    print(ids['my_id'])
    print(ids['name'])
    print(APIs)

    client = auto_follow_unfollow_module.apicall(APIs)

    ### 最新のJSONにする
    follower_dict = auto_follow_unfollow_module.follower_json_save(client=client, my_id=ids['my_id'], name=ids['name'])
    unfollow_list = auto_follow_unfollow_module.unfollow_id_only(name=ids['name'])

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
        auto_follow_unfollow_module.json_save(ids=new_unfollowing, json_name=f'/home/don/py/DMM/twitter_aff_videos/follow_auto/ura/{ids["name"]}_unfollow_done_id')
