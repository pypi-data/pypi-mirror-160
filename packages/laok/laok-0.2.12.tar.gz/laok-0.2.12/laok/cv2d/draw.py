#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/10 14:19:19

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['draw_text']

def draw_rect():
    pass

def draw_line():
    pass

def draw_circle():
    pass

def draw_ellipse():
    pass

def draw_polygon():
    pass

def draw_contours():
    pass

def draw_point():
    pass

def draw_detect_rect():
    pass

def draw_text(img, text, org=(100,100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.0, color=(0,0,255), thickness=1, lineType=cv2.LINE_AA):
    return cv2.putText(img, text, org = org, fontFace=fontFace, fontScale = fontScale,
                color=color, thickness=thickness, lineType=lineType, bottomLeftOrigin=False)