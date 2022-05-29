from master_twit_photo_upload import Tweet


if __name__ == '__main__':

    pic_dir = '/home/don/py/DMM/uraaka/yukarin_sef/yukarinn_0214/'

    i = Tweet()
    i.Uploads(account='yukarin_sef', password='asdflkjh', pic_dir=pic_dir)
    i.Quit()