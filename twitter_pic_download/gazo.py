import tweepy
import API_config_katudon
import json


class Tweet_text:

    def __init__(self):

        self.client = tweepy.Client(consumer_key=API_config_katudon.API_KEY, consumer_secret=API_config_katudon.API_SECRET, access_token=API_config_katudon.ACCESS_TOKEN, access_token_secret=API_config_katudon.ACCESS_TOKEN_SECRET, bearer_token=API_config_katudon.Bearer_token)
        self.count = 5


    @property
    def text_get(self):
        """_summary_
        usernameにアカウント名を入力

        画像を取る場合は以下を有効にする
        for tweets_img in target_tweets.includes['media']:

        """

        tweet: dict[dict] = {}
        tweet['tweet'] = []

        target_response = self.client.get_user(username='now_gravias') # usernameにアカウント名を入力
        target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=10, media_fields=['preview_image_url', 'url'], exclude='retweets')

        while True:
            print(target_tweets)
            next_token = target_tweets.meta['next_token']

            # テキストを取る
            for tweets in target_tweets.data:
                text = tweets.data['text']
                print(text)

            # 画像を取る
            for tweets_img in target_tweets.includes['media']:
                img_url = tweets_img['url']
                print(img_url)

            tweet['tweet'].append({"text": text,"img": img_url})
            print(tweet)

            with open('gidol.json', 'w', encoding='utf-8') as f:
                json.dump(tweet, f, indent=4, ensure_ascii=False)

            target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=10, media_fields=['preview_image_url', 'url'], exclude='retweets', pagination_token=next_token)

            if next_token is None:
                break



t = Tweet_text()
t.text_get


        # for tweets in tweepy.Paginator(self.client.get_users_tweets, target_response.data['id'], max_results=10, media_fields=['preview_image_url', 'url'], expansions=['attachments.media_keys'], tweet_fields=["entities"]).flatten(limit=250):
