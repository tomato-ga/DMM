import json

js = '/home/don/py/DMM/twitter_pic_api_test/new_mizugazo_all_photos.json'

j =  json.load(open(js))
print(len(j['photo']))


#TODO new_jsonをold_jsonに追加する