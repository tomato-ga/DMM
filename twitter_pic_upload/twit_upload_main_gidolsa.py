from master_twit_photo_upload import Tweet


if __name__ == '__main__':

    pic_dir = '/mnt/hdd/don/files/twitphotos/yukihira/'

    i = Tweet()
    i.Uploads(account='gidolsa', password='asdflkjh', text='#雪平莉左' + '\n' + '#かわいいと思ったらいいね' + '\n' + '#グラビア', pic_dir=pic_dir)
    i.Quit()

