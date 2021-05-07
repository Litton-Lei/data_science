# -*-coding:utf8 -*-
import imagehash
from PIL import Image
from cv2 import cv2 as cv2
from moviepy.editor import VideoFileClip


def isSimilar(img1, img2):
    # OpenCV图片转换为PIL image
    img1 = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

    # 通过imagehash获取两个图片的平均hash值
    n0 = imagehash.average_hash(img1)
    n1 = imagehash.average_hash(img2)

    # hash值最小相差多少则判断为不相似，可以根据需要自定义
    cutoff = 7

    print(f'目标帧hash平均值：{n0}')
    print(f'后一帧hash平均值：{n1}')
    print(f'hash差值：       {n0 - n1}')

    flag = True
    if n0 - n1 < cutoff:
        print('相似')
    else:
        flag = False
        print('不相似')
    return flag


def sliceVideo(clip, fps):
    im0 = ""  # 目标帧
    start_time = 0  # 片段开始时间
    end_time = 0  # 片段结束时间
    success_durations = []  # 成功片段时间列表
    skip_durations = []  # 排除片段时间列表
    for i, img in enumerate(clip.iter_frames(fps)):
        if i == 0: im0 = img
        time = (i) / fps
        print(f'n第{time}秒')
        result = isSimilar(im0, img)
        if not result:  # 结果为不相似
            end_time = (i - 1) / fps
            print(start_time, end_time)
            if start_time == end_time:  # 排除情况，开始时间和结束时间相同的话moviepy会报错；也可以根据需要筛选时长大于多少的片段
                skip_durations.append([start_time, end_time])
            else:
                clip.subclip(start_time, end_time).write_videofile(f"SUBCLIP-{i}.mp4")
                success_durations.append([start_time, end_time])
            start_time = time
        im0 = img
    # 前面的循环并没有包括视频中最后一段画面，因此需要在最后加上
    end_time = clip.duration
    if start_time == end_time:  # 排除情况
        skip_durations.append([start_time, end_time])
    else:
        clip.subclip(start_time, end_time).write_videofile(f"SUBCLIP-{i}.mp4")
        success_durations.append([start_time, end_time])

    return success_durations, skip_durations


if __name__ == "__main__":


    clip = VideoFileClip("demo.mp4")
    success, skip = sliceVideo(clip, clip.fps)
    print(f"成功片段：n{success}nn排除片段：n{skip}n")