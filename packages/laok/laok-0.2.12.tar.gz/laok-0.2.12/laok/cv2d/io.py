#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/24 21:29:16

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import cv2
import numpy as np
from .cvt import keep_bgr, keep_gray, image_size, is_color
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['read_cv_color', 'read_cv_gray', 'read_pil_img',
           'write_cv_img', 'read_cv_video', 'read_cv_camera',
           'VideoWriter',
           ]

####################    读取图像
def _read_cv_img(file, flags):
    return cv2.imdecode(np.fromfile(file, dtype=np.uint8), flags)

def read_cv_color(file):
    return _read_cv_img(file, cv2.IMREAD_COLOR)

def read_cv_gray(file):
    return _read_cv_img(file, cv2.IMREAD_GRAYSCALE)

def read_pil_img(file):
    from PIL import Image
    return Image.open(file)

def write_cv_img(file, data):
    name, ext = os.path.splitext(file)
    retval, buf = cv2.imencode(ext, data)
    return buf.tofile(file)

####################    读取视频和相机
def _read_cv_capture(fileOrId):
    try:
        cap = cv2.VideoCapture(fileOrId)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame
    finally:
        cap.release()

def read_cv_video(video_file):
    for frame in _read_cv_capture(video_file):
        yield frame

def read_cv_camera(camId = 0):
    for frame in _read_cv_capture(camId):
        yield frame


class VideoWriter:
    def __init__(self, filename, fourcc="mp4v", fps=24, frameSize=None, isColor=None):
        self.filename_ = filename
        self.frameSize_ = frameSize
        self.isColor_ = isColor
        self.fps_ = fps
        self.fourcc_ =  cv2.VideoWriter_fourcc(*fourcc)
        self.writer_ = None

    def _make_video(self, img):
        if self.frameSize_ is None:
            self.frameSize_ = image_size(img)

        if self.isColor_ is None:
            self.isColor_ = is_color(img)

        self.writer_ = cv2.VideoWriter(filename=self.filename_, fourcc=self.fourcc_,
                                      fps=self.fps_, frameSize=self.frameSize_, isColor=self.isColor_)

    def write(self, img):
        if self.writer_ is None:
            self._make_video(img)

        if self.isColor_ :
            img = keep_bgr(img)
        else:
            img = keep_gray(img)

        if image_size(img) != self.frameSize_:
            img = cv2.resize(img, dsize=(self.frameSize_[0], self.frameSize_[1]), interpolation=cv2.INTER_LINEAR)

        self.writer_.write(img)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.writer_ is not None:
            self.writer_.release()
