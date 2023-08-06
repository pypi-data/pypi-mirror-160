#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/25 21:57:25

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2, numpy as np
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['edge_laplace', 'edge_canny',
           'edge_sobel_x', 'edge_sobel_y', 'edge_sobel']

def edge_laplace(img, ksize=1, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT):
    return cv2.Laplacian(img, ddepth = -1, ksize=ksize, scale=scale, delta=delta, borderType=borderType)


def edge_canny(grayImg, threshold1 = 50,  threshold2 = 150, apertureSize=3, L2gradient=False):
    return cv2.Canny(grayImg, threshold1 = threshold1, threshold2 = threshold2, apertureSize=apertureSize, L2gradient=L2gradient)

def edge_sobel_x(img, ksize=0, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT):
    return cv2.Sobel(img, cv2.CV_16S, dx=1, dy=0, ksize=ksize, scale=scale, delta=delta, borderType=borderType)

def edge_sobel_y(img, ksize=0, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT):
    return cv2.Sobel(img, cv2.CV_16S, dx=0, dy=1, ksize=ksize, scale=scale, delta=delta, borderType=borderType)

def edge_sobel(img, res_type='none', ksize=0, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT):
    ''' res_type: 'none', 'trunc', 'abs'
    '''
    x_img = cv2.Sobel(img, cv2.CV_16S, dx=1, dy=0, ksize=ksize, scale=scale, delta=delta, borderType=borderType)
    y_img = cv2.Sobel(img, cv2.CV_16S, dx=0, dy=1, ksize=ksize, scale=scale, delta=delta, borderType=borderType)
    if res_type == 'trunc':
        res = np.clip(x_img, 0, 255)  + np.clip(y_img, 0, 255)
    elif res_type == 'abs':
        res = np.abs(x_img) + np.abs(y_img)
    else:
        res = x_img + y_img
    return cv2.normalize(res, dst=res, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)