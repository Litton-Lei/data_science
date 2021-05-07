# -*-coding:UTF-8 -*-
# import youtube_dl

import os

# 不下载youtube视频，下载视频中文字幕
os.system(command='youtube-dl '
                  '--skip-download '
                  '--write-auto-sub '
                  '--sub-lang zh-Hans '
                  '--sub-format srt '
                  '--convert-subtitles '
                  'srt https://www.youtube.com/watch?v=qvNyo1-AK6o')

# 下载YouTube视频，视频嵌入自动翻译的中文字幕
def command(url):
    os.system(command='youtube-dl '
                      '--write-auto-sub '
                      '--sub-lang zh-Hans '
                      '--embed-sub '
                      '--convert-subtitles srt '
                      '--recode-video mp4 '
                      '-f bestvideo+bestaudio '
                      '-o "H:\\ML&DL_fundamentals\\%(title)s.%(format)s" '
                      f'-i {url} ')

# 仅下载YouTube视频，最好的视频，不带背景音乐
os.system(command='youtube-dl -f bestvideo https://www.youtube.com/watch?v=iJvr0VPsn-s')