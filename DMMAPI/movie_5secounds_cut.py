from moviepy.editor import *
import os
import random

def cut5secounds(directory):

    vs = os.listdir(directory)
    random.shuffle(vs)
    file = os.path.abspath(directory + vs[0])

    #ビデオパスを入れる
    save_file_name = 'cuttest.mp4' #保存ファイル名
    start = 5

    videos = VideoFileClip(file).subclip(start)
    videos.write_videofile(save_file_name, fps=29, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)


def cut2min():

    video_path = '/Users/ore/Downloads/[FRIDAY] Risa Yukihira 雪平莉左 - Do you like a beautiful older sister 綺麗なお姉さんは、好きですか？ (2021-11-18)/yukihira.ts' #ビデオパスを入れる
    save_file_name = 'cuttest.mp4' #保存ファイル名
    start = 5

    videos = VideoFileClip(video_path).subclip(start)
    videos.write_videofile(save_file_name, fps=29)


dir = '/mnt/hdd/don/files/menes_fanza_video/'
cut5secounds(dir)