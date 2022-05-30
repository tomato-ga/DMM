import auto_follow_unfollow_module
import os
import api_OtxSf
import api_togsi7
import api_HjQhq
import api_1j_mc

"""
my_idとnameにアカウントIDと名前を入れる
"""


max_count = 15
get_dir = os.getcwd()
print(get_dir)

id_name_listdict = [
    {
        'my_id': 1515978583730458630,
        'name': 'OtxSf',
        },
    {
        'my_id': 1515697390480945160,
        'name': '1j_mc',
        },
    {
        'my_id': 1515514246775582722,
        'name': 'HjQhq',
        },
    {
        'my_id': 1515696887781015558,
        'name': 'togsi',
        }
    ]


for ids, APIs in zip(id_name_listdict, [api_OtxSf, api_1j_mc, api_HjQhq, api_togsi7]):
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
            auto_follow_unfollow_module.json_save(ids=follow_dict, json_name=f'/home/don/py/DMM/twitter_aff_videos/follow_auto/main/{ids["name"]}_following_id')
