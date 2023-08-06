#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/26 11:04:35

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import types
from pathlib import Path
import cv2, numpy as np
from laok.cv2d.gui import show, show_wait
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['read_smaple_img', 'run_sample_image']

def read_smaple_img(is_color=True):
    fPath = Path(__file__).parent.joinpath('lena.jpg')
    flags = cv2.IMREAD_COLOR if is_color else cv2.IMREAD_GRAYSCALE
    return cv2.imdecode(np.fromfile(fPath, dtype=np.uint8), flags=flags)

def _get_name(trans):
    if hasattr(trans, '__name__'):
        return trans.__name__
    if hasattr(trans, 'func'):
        return trans.func.__name__
    if hasattr(trans, '__class__'):
        return trans.__class__.__name__

def run_sample_image(trans, is_color=True):
    img = read_smaple_img(is_color)
    img_trans = trans(img)
    show(img_trans, _get_name(trans))
    show_wait(img)
