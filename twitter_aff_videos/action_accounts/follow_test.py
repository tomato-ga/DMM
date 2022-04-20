import tweepy
import time
import random
from tweepy import TweepyException


# ここに自分のアカウントのID(@以降)とAPI鍵・アクセストークンを入力する
api_dict = {
            'my_account_id': 
                [
                'api_pub',
                'api_sec',
                'access_token',
                'access_token_secret'
                ]
            }

# フォローしていなくても外さないアカウントのリスト（リストの中身は例）
unrequited_list = {
    'my_account_id':
        [
            'MSkieller',
            'BitcoinSVinfo',
            '_unwriter',
            'excalibur0922',
            'money_button'
        ]
        }

#複数のアカウントで運用するためにfor文で回す
for k, v in api_dict.items():
    consumer_key = v[0]
    consumer_secret = v[1]
    access_token = v[2]
    access_secret = v[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    #自分のuserid
    userid = k

    try:
        #自分のアカウントのフォロワーをすべて取得する
        followers_id = api.followers_ids(userid)

        #自分のアカウントのフォロイングをすべて取得する
        following_id = api.friends_ids(userid)

        #フォローされていなくてもOKなアカウントの情報をIDから取得
        unrequited = unrequited_list[k]
        for i in unrequited:
            try:
                sp_id = api.get_user( id = i)._json['id']
                followers_id.append(sp_id)
            except Exception as e:
                print(i, e.args)

        # API制限などのカウント用変数を定義
        api_limit = 0
        api_limit_f = 0
        unfollow_user = 0
        follow_user = 0

        # 相互じゃないユーザーのフォローを解除する
        for following in following_id:
            if following not in followers_id and api_limit < 25:
                time.sleep(random.randrange(1,10,1))
                user  = api.get_user( id = following)
                userfollowers  = user.followers_count

                # フォロワー数が10000人以下で自分をフォローしていないユーザーを除外する
                if userfollowers < 10000:
                    time.sleep(random.randrange(2,30,2))
                    username = user.name
                    print("リムーブするユーザー名", username)
                    print("フォロワー数", userfollowers)
                    # フォローを外す
                    time.sleep(random.randrange(2,20,2))
                    api.create_mute( id = following) #ミュート
                    time.sleep(random.randrange(2,20,2))
                    api.create_block( id = following) #ブロック
                    #api.destroy_friendship( id = following) #リムーブ用
                    api_limit += 1
                    unfollow_user += 1
                    time.sleep(random.randrange(2,20,2))

        for follower in followers_id:
            # フォローを返していないユーザーにフォローを返す
            if follower not in following_id and api_limit_f < 25:
                time.sleep(random.randrange(1,10,1))
                print("checkユーザーID", follower)
                #鍵アカウントチェック
                try:
                    user = api.get_user( id = follower)
                except TweepyException as e:
                    print(e)
                    continue

                userfollowers = user.followers_count
                print("checkユーザーfollower", userfollowers)
                # フォロワー数が10人以下はフォロバしない
                if userfollowers > 10:
                    try:
                        time.sleep(random.randrange(2,20,2))
                        username = user.name
                        print("フォローするユーザー名", username)
                        time.sleep(random.randrange(2,20,2))
                        api.create_friendship(follower)
                        api_limit_f += 1
                        follow_user += 1
                        time.sleep(random.randrange(2,20,2))
                    except Exception as e:
                        e_msg = e.args[0][0]['code']
                        # api制限に引っかかった場合（Code161）はループ終了
                        if e_msg == 161:
                            break
                        # それ以外の場合はエラーメッセージを表示
                        else:
                            print(e.args)

        print(f'リムったユーザーは{unfollow_user}人です')
        print(f'フォローしたユーザーは{follow_user}人です')

    except Exception as e:
        print(f'{k}のAPI操作でエラーが発生しました')
        print(e.args)
