from master_twit_photo_upload import Tweet
import random
import os

"""
'#新垣結衣': '/mnt/hdd/don/files/mizugazo/新垣結衣/' ← スラッシュ忘れないこと
"""

if __name__ == '__main__':

    photos = {
    '#貴島明日香': '/mnt/hdd/don/files/mizugazo/貴島明日香/',
    '#桃月なしこ': '/mnt/hdd/don/files/mizugazo/桃月なしこ/',
    '#福田ルミカ': '/mnt/hdd/don/files/mizugazo/福田ルミカ/',
    '#本郷柚巴': '/mnt/hdd/don/files/mizugazo/本郷柚巴/',
    '#沢口愛華': '/mnt/hdd/don/files/mizugazo/沢口愛華/',
    '#ばんばんざいるな': '/mnt/hdd/don/files/mizugazo/ばんばんざいるな/',
    '#賀喜遥香': '/mnt/hdd/don/files/mizugazo/賀喜遥香/',
    '#吉岡里帆': '/mnt/hdd/don/files/mizugazo/吉岡里帆/',
    '#橋本環奈': '/mnt/hdd/don/files/mizugazo/橋本環奈/',
    # '#新垣結衣': '/mnt/hdd/don/files/mizugazo/新垣結衣/',
    # '#鷲見玲奈': '/mnt/hdd/don/files/mizugazo/鷲見玲奈/',
    # '#小芝風花': '/mnt/hdd/don/files/mizugazo/小芝風花/',
    #'#今田美桜': '/mnt/hdd/don/files/twitphotos/_mio_mio_imada/',
    #'#馬場ふみか': '/mnt/hdd/don/files/twitphotos/HoretaFumika/',
    #'#横野すみれ': '/mnt/hdd/don/files/mizugazo/横野すみれ/',
    #'#浅川梨奈': '/mnt/hdd/don/files/mizugazo/浅川梨奈/',
    #'#宮脇咲良': '/mnt/hdd/don/files/mizugazo/宮脇咲良/',
    #'#岸明日香': '/mnt/hdd/don/files/mizugazo/岸明日香/',
    # '#山本舞香': '/mnt/hdd/don/files/mizugazo/山本舞香/',
    }

    hashtag, pic_dir = random.choice(list(photos.items()))
    assert os.path.isdir(pic_dir)
    print(hashtag, pic_dir)


    i = Tweet()
    i.Uploads(account='gidolsa', password='asdflkjh', text=hashtag + '\n' + '#かわいいと思ったらいいね' + '\n' + '#グラビア', pic_dir=pic_dir)
    i.Quit()

