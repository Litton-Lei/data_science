# -*-coding:utf8 -*-

"""裁剪图片"""

import os

import cv2
from tqdm import tqdm

for root,dit,files in os.walk('./'):
    for file in tqdm(files[0:-1]):
        img=cv2.imread('./{}'.format(file))
        hight = int(img.shape[0])
        width = int(img.shape[1])
        cut = img[int(0 * hight):int(0.93 * hight), int(0 * width):int(1 * width)]
        cv2.imwrite(file,cut)


