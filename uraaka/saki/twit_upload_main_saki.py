from master_twit_photo_upload import Tweet

if __name__ == '__main__':

    pic_dir = '/home/don/py/DMM/uraaka/saki/saki/'

    i = Tweet()
    i.Uploads(account='sakki0808', password='asdflkjh', pic_dir=pic_dir)
    i.Quit()