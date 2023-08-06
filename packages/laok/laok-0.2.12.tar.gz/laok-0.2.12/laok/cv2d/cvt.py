#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/6 11:06:36

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
import numpy as np
#===============================================================================
'''  
# skimage 图像格式        通道：RGB 像素值：[0.0,1.0]      (h,w)
    
# Opencv  图像格式        通道：BGR 像素值：[0,255]        (h,w)
    gray是 (h,w)  
    color是(h,w,3)
# PIL     图像格式        (w,h)   
    
'''
#===============================================================================

__all__  = ['gray2bgr', 'gray2rgb',
            'bgr2gray', 'rgb2gray',
            'swap_rb',
            'cv2pil', 'pil2cv', 'cv2sk', 'sk2cv', 'pil2sk', 'sk2pil',
            'normlize_uint8', 'normlize_float32',
            'is_color', 'is_gray',
            'keep_bgr', 'keep_gray',
            'image_size', 'resize_abs', 'resize_rel'
            ]

def gray2bgr(img):
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img

def gray2rgb(img):
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img

def bgr2gray(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    return img

def rgb2gray(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY )
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY )
    return img

def swap_rb(img):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def cv2pil(img):
    from PIL import Image
    if img.ndim == 3 and img.shape[-1] == 3:
        img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB), mode = 'RGB')
    else:
        img = Image.fromarray(img, mode = 'L')
    return img

def pil2cv(img):
    if img.mode == 'RGB':
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    elif img.mode == 'RGBA':
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
    elif img.mode == 'L':
        image = np.asarray(img)
    return image

def cv2sk(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGBA)
    return img

def sk2cv(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img,cv2.COLOR_RGBA2BGRA)
    return img

def pil2sk(img):
    pass

def sk2pil(img):
    pass

def is_color(img):
    if img.ndim == 3:
        return img.shape[-1] > 1
    return False

def is_gray(img):
    return not is_color(img)

def normlize_uint8(mat, alpha=0, beta=255):
    return cv2.normalize(mat, dst=None, alpha=alpha, beta=beta, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

def normlize_float32(mat, alpha=0, beta=1):
    return cv2.normalize(mat, dst=None, alpha=alpha, beta=beta, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

def normlize_int32(mat, alpha=0, beta=255):
    return cv2.normalize(mat, dst=None, alpha=alpha, beta=beta, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32S)

def keep_gray(img):
    if is_color(img):
        return bgr2gray(img)
    return img

def keep_bgr(img):
    if is_gray(img):
        return gray2bgr(img)
    return img

def image_size(img):
    return (img.shape[1], img.shape[0])

def resize_abs(img, width, height, interpolation=cv2.INTER_LINEAR):
    return cv2.resize(img, dsize=(int(width), int(height)), interpolation=interpolation)

def resize_rel(img, fx= 0.5, fy = 0, interpolation=cv2.INTER_LINEAR):
    if fy == 0:
        fy = fx
    return cv2.resize(img, fx=fx, fy=fy, interpolation=interpolation)
