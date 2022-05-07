import tweepy
import API_config_katudon
import json


class Tweet_text:

    def __init__(self):
        self.client = tweepy.Client(consumer_key=API_config_katudon.API_KEY, consumer_secret=API_config_katudon.API_SECRET, access_token=API_config_katudon.ACCESS_TOKEN, access_token_secret=API_config_katudon.ACCESS_TOKEN_SECRET, bearer_token=API_config_katudon.Bearer_token, wait_on_rate_limit=True)

    def text_get(self, username):
        tweet = {}
        tweet['tweet'] = []

        target_response = self.client.get_user(username=username)
        target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=100, media_fields=['preview_image_url', 'url'], exclude='retweets')

        while True:
            print(target_tweets)
            next_token = target_tweets.meta['next_token'] #pagination token取得

            for tweets in target_tweets.data:
                text = tweets.data['text']
                print(text)

            for tweets_img in target_tweets.includes['media']:
                img_url = tweets_img['url']
                print(img_url)

            tweet['tweet'].append({"text": text,"img": img_url})
            print(tweet)

            with open(f'{username}.json', 'w', encoding='utf-8') as f:
                json.dump(tweet, f, indent=4, ensure_ascii=False)

            target_tweets = self.client.get_users_tweets(target_response.data['id'], expansions=["attachments.media_keys"], max_results=10, media_fields=['preview_image_url', 'url'], exclude='retweets', pagination_token=next_token) # next tokenがあったら再取得

            if next_token is None: # next tokenがなくなったらbreak
                break

if __name__ == '__main__':

    username = '_mio_mio_imada'

    t = Tweet_text()
    t.text_get(username)


        # for tweets in tweepy.Paginator(self.client.get_users_tweets, target_response.data['id'], max_results=10, media_fields=['preview_image_url', 'url'], expansions=['attachments.media_keys'], tweet_fields=["entities"]).flatten(limit=250):
