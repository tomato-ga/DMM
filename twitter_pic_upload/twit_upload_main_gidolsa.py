from master_twit_photo_upload import Tweet
import meigen_jan
import random

if __name__ == '__main__':

    meigens: list[str] = meigen_jan.m
    random.shuffle(meigens)

    for meigen in meigens:
        text = meigen

    i = Tweet()
    i.Uploads(account='gidolsa', text=f'{text}' + '\n' + '#グラビア')
    i.Quit()



