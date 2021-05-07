
# -*-coding:utf8 -*-
"""转换视频分辨率"""
import cv2
cap = cv2.VideoCapture("10236_飞机着陆后视图.mp4")
videowriter = cv2.VideoWriter("videl_"+".mp4", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (1920,1080))
success, _ = cap.read()
while success:
    success, img1 = cap.read()
    try:
         img = cv2.resize(img1, (1920,1080), interpolation=cv2.INTER_CUBIC)
         videowriter.write(img)
    except:
         break

