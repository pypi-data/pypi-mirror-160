#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/29 17:22:41

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2, numpy as np
#===============================================================================
'''     
'''
#===============================================================================

__all__ = ['show', 'show_wait', 'wait']

def show(mat, winname='img', winflag = cv2.WINDOW_NORMAL, title = None):
    cv2.namedWindow(winname, winflag)
    if title:
        cv2.setWindowTitle(winname, title)
    if mat.dtype == np.bool: #转换bool 类型
        mat = mat.astype(np.uint8) * 255
    elif mat.dtype != np.uint8:  # 转换 其它类型
        mat = cv2.normalize(mat, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow(winname, mat)

def wait(delay=0):
    key = cv2.waitKey(delay)
    if key == 27: # 'Esc' to quit
        quit()

def show_wait(mat, winname='img', delay=0, winflag = cv2.WINDOW_NORMAL, title = None):
    show(mat, winname=winname, winflag=winflag, title=title)
    wait(delay=delay)
