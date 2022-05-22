from heapq import merge
import json
import pandas as pd

old_json = json.load(open('/home/don/py/DMM/twitter_pic_api_test/old_mizugazo_all_photos.json', 'r'))
new_json = json.load(open('/home/don/py/DMM/twitter_pic_api_test/new_mizugazo_all_photos.json', 'r'))


old_df = pd.DataFrame(old_json['photo'])
new_df = pd.DataFrame(new_json['photo'])


merge_df = pd.merge(old_df, new_df)
print(merge_df)