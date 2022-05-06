from master_twit_photo_upload import Tweet
import random
import os

############################ディレクトリ指定############################

pic_dir = '/mnt/hdd/don/files/twitphotos/yukihira/'  # '/mnt/hdd/don/files/twitphotos_gurasen/' #'E:\\twit_photos_gurasen\\'
# pic_subdir = os.listdir(pic_dir) # サブディレクトリ一覧
# random.shuffle(pic_subdir) # サブディレクトリをランダム化
photo_lists = os.listdir(pic_dir) # 画像ファイル一覧
random.shuffle(photo_lists) # 画像ファイル一覧をランダム化
up_photo = os.path.abspath(pic_dir + photo_lists[0])  # Win (pic_dir + pic_subdir[0] + '\\' + photo_lists[0]) # アップするファイルパス取得

############################ディレクトリ指定############################

if __name__ == '__main__':

    print(photo_lists)
    print(up_photo)
    i = Tweet()
    i.Uploads(account='gidolsa', text='#雪平莉左' + '\n' + '#かわいいと思ったらいいね',  up_photo=up_photo)
    i.Quit()



