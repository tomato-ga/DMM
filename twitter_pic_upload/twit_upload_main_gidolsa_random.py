from master_twit_photo_upload import Tweet
import random


if __name__ == '__main__':

    photos = {
    '#今田美桜': '/mnt/hdd/don/files/twitphotos/_mio_mio_imada/',
    '#馬場ふみか': '/mnt/hdd/don/files/twitphotos/HoretaFumika/'
    }


    hashtag, pic_dir = random.choice(list(photos.items()))
    print(hashtag, pic_dir)


    i = Tweet()
    i.Uploads(account='gidolsa', password='asdflkjh', text=hashtag + '\n' + '#かわいいと思ったらいいね' + '\n' + '#グラビア', pic_dir=pic_dir)
    i.Quit()

