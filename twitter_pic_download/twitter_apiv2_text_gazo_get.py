import tweepy
import API_config_katudon
import json


class Tweet_text:

    def __init__(self):

        self.client = tweepy.Client(consumer_key=API_config_katudon.API_KEY, consumer_secret=API_config_katudon.API_SECRET, access_token=API_config_katudon.ACCESS_TOKEN, access_token_secret=API_config_katudon.ACCESS_TOKEN_SECRET, bearer_token=API_config_katudon.Bearer_token)
        self.count = 5


    def text_media_get(self, username):
        """_summary_
        usernameにアカウント名を入力

        画像を取る場合は以下を有効にする
        for tweets_img in target_tweets.includes['media']:

        """

        tweet: dict[dict] = {}
        tweet['tweet'] = []

        target_response = self.client.get_user(username=username)
        target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=10, media_fields=['preview_image_url', 'url'], exclude=['retweets', 'replies'])
        next_token = target_tweets.meta['next_token']

        while True:
            print(target_tweets)

            try:

                # テキストを取る
                for tweets in target_tweets.data:
                    text = tweets.data['text']
                    tweet['tweet'].append({"text": text})
                    print(text)

                # 画像を取る
                if target_tweets.includes:
                    for tweets_img in target_tweets.includes['media']:
                        img_url = tweets_img['url']
                        print(img_url)

                    tweet['tweet'].append({"img": img_url})
                    print(tweet)

                target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=10, media_fields=['preview_image_url', 'url'], exclude=['retweets', 'replies'], pagination_token=next_token)
                next_token = target_tweets.meta['next_token']
            except KeyError as e:
                print(e)
                break


        return tweet


username = 'sumire_ma2'
t = Tweet_text()
tweet = t.text_media_get(username)

with open(f'/home/don/py/DMM/twitter_pic_download/tweet_{username}.json', 'w', encoding='utf-8') as f:
            json.dump(tweet, f, indent=4, ensure_ascii=False)


        # for tweets in tweepy.Paginator(self.client.get_users_tweets, target_response.data['id'], max_results=10, media_fields=['preview_image_url', 'url'], expansions=['attachments.media_keys'], tweet_fields=["entities"]).flatten(limit=250):
