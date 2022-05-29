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

                name_search = re.findall('([a-zA-z0-9_-]*)(.[a-z]{3,4}$)', image_url)
                file_ex =  name_search[0][1]

                print(tweet)

                img_response = requests.get(image_url)
                match img_response.status_code:
                    case 200:
                        os.makedirs(f'/home/don/py/DMM/twitter_pic_download/{self.__username}', mode=0o777, exist_ok=True)
                        with open(f'/home/don/py/DMM/twitter_pic_download/{self.__username}/{index}{file_ex}', 'wb') as image:
                            image.write(img_response.content)

                        tweet['tweet'].append({"text": tweet_text, 'img': image_url, 'img_file': f'{index}.jpg'})
                        index += 1

                # with open(f'/home/don/py/DMM/twitter_pic_download/{self.__username}.json', 'w', encoding='utf-8') as f:
                #     json.dump(tweet, f, indent=4, ensure_ascii=False)

            elif 'media' not in result.entities:
                texts = result.full_text
                text = texts.split()
                tweet_text = text[0]
                print(tweet_text)

                tweet['tweet'].append({"text": tweet_text})
                index += 1

            else:
                pass

        with open(f'/home/don/py/DMM/twitter_pic_download/{self.__username}.json', 'w', encoding='utf-8') as f:
            json.dump(tweet, f, indent=4, ensure_ascii=False)

# ID入れる
t = Tweet_text('yukarinn_0214')
t.text_image_get_tojson()