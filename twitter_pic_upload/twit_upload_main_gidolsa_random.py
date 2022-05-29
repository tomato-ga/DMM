from master_twit_photo_upload import Tweet
import random
import os


if __name__ == '__main__':

    photos = {
    '#今田美桜': '/mnt/hdd/don/files/twitphotos/_mio_mio_imada/',
    '#馬場ふみか': '/mnt/hdd/don/files/twitphotos/HoretaFumika/',
    '#横野すみれ': '/mnt/hdd/don/files/mizugazo/横野すみれ/',
    '#浅川梨奈': '/mnt/hdd/don/files/mizugazo/浅川梨奈/',
    '#新垣結衣': '/mnt/hdd/don/files/mizugazo/新垣結衣/',
    '#宮脇咲良': '/mnt/hdd/don/files/mizugazo/宮脇咲良/',
    '#岸明日香': '/mnt/hdd/don/files/mizugazo/岸明日香/',
    '#貴島明日香': '/mnt/hdd/don/files/mizugazo/貴島明日香/',
    '#佐野ひなこ': '/mnt/hdd/don/files/mizugazo/佐野ひなこ/'
    }

    hashtag, pic_dir = random.choice(list(photos.items()))
    print(hashtag, pic_dir)


    i = Tweet()
    i.Uploads(account='gidolsa', password='asdflkjh', text=hashtag + '\n' + '#かわいいと思ったらいいね' + '\n' + '#グラビア', pic_dir=pic_dir)
    i.Quit()

