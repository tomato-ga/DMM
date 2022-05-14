from moviepy.editor import *

def cut5secounds():

    video_path = 'C:\\Users\\PC_User\\Documents\\GitHub\\DMM\\23test.mp4' #ビデオパスを入れる
    save_file_name = 'cuttest.mp4' #保存ファイル名
    start = 5

    videos = VideoFileClip(video_path).subclip(start)
    videos.write_videofile(save_file_name, fps=29)


def cut2min():

    video_path = '/Users/ore/Downloads/[FRIDAY] Risa Yukihira 雪平莉左 - Do you like a beautiful older sister 綺麗なお姉さんは、好きですか？ (2021-11-18)/yukihira.ts' #ビデオパスを入れる
    save_file_name = 'cuttest.mp4' #保存ファイル名
    start = 5

    videos = VideoFileClip(video_path).subclip(start)
    videos.write_videofile(save_file_name, fps=29)

