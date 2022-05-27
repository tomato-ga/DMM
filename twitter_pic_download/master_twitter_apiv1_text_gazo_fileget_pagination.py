import tweepy
import API_config_katudon
import json
import requests
import re
import os


class Tweet_text:
    """v1"""

    def __init__(self, username):

        auth = tweepy.OAuthHandler(API_config_katudon.API_KEY, API_config_katudon.API_SECRET)
        auth.set_access_token(API_config_katudon.ACCESS_TOKEN, API_config_katudon.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.__username = username

    def text_image_get_tojson(self):


        count_no = 5000
        tweet: dict[dict] = {}
        tweet['tweet'] = []

        results: iter = tweepy.Cursor(self.api.user_timeline, # タイムラインの取得
                    id=self.__username, # 取得対象のユーザーを指定
                    include_entities=True, # 省略されたリンクを全て取得
                    tweet_mode='extended', # 省略されたツイートを全て取得
                    lang='ja',
                    exclude_replies=False,
                    include_rts=False).items(limit=count_no) # 取得件数を指定

        index = 1

        for result in results:
            if 'media' in result.entities:
                image_url = result.extended_entities['media'][0]['media_url']
                texts = result.full_text
                text = texts.split()
                tweet_text = text[0]

                print(tweet)

                img_response = requests.get(image_url)
                match img_response.status_code:
                    case 200:
                        os.makedirs(f'/home/don/py/DMM/twitter_pic_download/{self.__username}', mode=0o777, exist_ok=True)
                        with open(f'/home/don/py/DMM/twitter_pic_download/{self.__username}/{index}.jpg', 'wb') as image:
                            image.write(img_response.content)

                        tweet['tweet'].append({"text": tweet_text, 'img': image_url, 'img_file': f'{index}.jpg'})
                        index += 1

                with open(f'/home/don/py/DMM/twitter_pic_download/{self.__username}.json', 'w', encoding='utf-8') as f:
                    json.dump(tweet, f, indent=4, ensure_ascii=False)



ids = [
    'keikooobot',
    'kitagawa_kg',
    'ayaaabot',
    'ayase_haruka_ch',
    'woqyvyqerixe',
    'keiko_matome',
    'keiko_gazou',
    'kikktgw_info',
    'Satomi_pic',
    'LOVE39895347',
    'tubasa_lovebot',
    'kasumi_pic',
    'kurasina_gazou',
]

for id in ids:
    t = Tweet_text(id)

#t = Tweet_text('hinachimuu_pic')
    t.text_image_get_tojson()






# erika_1837 裏垢