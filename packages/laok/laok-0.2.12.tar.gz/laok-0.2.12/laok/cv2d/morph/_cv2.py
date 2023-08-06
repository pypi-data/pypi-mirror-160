#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/26 10:16:16

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['morph_close', 'morph_open', 'morph_blackhat',
           'morph_dilate', 'morph_erode', 'morph_gradient',
           'morph_hitmiss', 'morph_tophat']

def _morph_impl(img, op, ksize=(3, 3), shape=cv2.MORPH_RECT, anchor=(-1, -1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)):
    kernel = cv2.getStructuringElement(shape=shape, ksize=ksize, anchor=anchor)
    return cv2.morphologyEx(img, op=op, kernel=kernel, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_close(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_CLOSE, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_open(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_OPEN, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_dilate(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_DILATE, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_erode(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_ERODE, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_gradient(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_GRADIENT, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_tophat(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_TOPHAT, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_blackhat(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_BLACKHAT, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

def morph_hitmiss(img, ksize=(3,3), shape=cv2.MORPH_RECT, anchor=(-1,-1), iterations=1, borderType=cv2.BORDER_CONSTANT, borderValue=(0,0,0)):
    return _morph_impl(img, op=cv2.MORPH_HITMISS, ksize=ksize, shape=shape, anchor=anchor, iterations=iterations, borderType=borderType, borderValue=borderValue)

