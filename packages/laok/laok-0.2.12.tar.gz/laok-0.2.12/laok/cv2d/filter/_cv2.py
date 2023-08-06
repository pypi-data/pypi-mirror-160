#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/26 00:43:37

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2, numpy as np
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['filter_blur', 'filter_gauss', 'filter_bilateral', 'filter_median',
           ]

def filter_blur(img, ksize=(3,3), anchor=(-1,-1), borderType=cv2.BORDER_DEFAULT):
    return cv2.blur(img, ksize=ksize, anchor=anchor, borderType=borderType)

def filter_gauss(img, ksize, sigmaX, sigmaY=None, borderType=None):
    return cv2.GaussianBlur(img, ksize=ksize, sigmaX=sigmaX, sigmaY=sigmaY, borderType=borderType)

def filter_bilateral():
    pass

def filter_median():
    pass

def filter_meansift():
    pass

