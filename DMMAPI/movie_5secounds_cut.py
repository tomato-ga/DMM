from moviepy.editor import *

def cut5():

    video_path = 'C:\\Users\\PC_User\\Documents\\GitHub\\DMM\\23test.mp4' #ビデオパスを入れる
    save_file_name = 'cuttest.mp4' #保存ファイル名
    start = 5

    videos = VideoFileClip(video_path).subclip(start)
    videos.write_videofile(save_file_name, fps=29)
