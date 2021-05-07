# -*-coding:utf8 -*-
"""修改图片的Exif信息"""

import PIL
import piexif
from PIL import Image

new_im = PIL.Image.open(r'./SW001.JPG')

zeroth_ifd = {piexif.ImageIFD.XPTitle: u"环球素材库".encode('utf-16'),
              # piexif.ImageIFD.XPComment: u''.encode('utf-16'),
              piexif.ImageIFD.XPAuthor: u"Litton".encode('utf-16'),
              piexif.ImageIFD.Copyright: u'© Copyright belongs to Litton'.encode('utf-8'),
              }
exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u"2020:09:29 10:10:10"}

exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
exif_bytes = piexif.dump(exif_dict)
new_im.save(r'out.jpg', exif=exif_bytes)

