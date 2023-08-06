#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/29 08:10:41

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import numpy as np
from ..statis import cld_bounding_box
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['proj_img_x_div', 'proj_img_y_div', 'proj_img_z_div']

def proj_img_x_div(cld, div=200):
    ind = 0
    minPt, maxPt = cld_bounding_box(cld)
    resolution = (maxPt - minPt) / (div - 1)
    resolution[ind] = 1
    cldXYZ = (cld[:, 0:3] - minPt) / resolution
    _fill = minPt[ind] - (maxPt[ind] - minPt[ind])
    img = np.full((div, div), fill_value=_fill, dtype=np.float32)
    for xyz in cldXYZ:
        y = int(xyz[1])
        z = int(xyz[2])
        img[z,y] = xyz[0]
    return img

def proj_img_z_div(cld, div=200):
    ind = 2
    minPt, maxPt = cld_bounding_box(cld)
    resolution = (maxPt - minPt) / (div - 1)
    resolution[ind] = 1
    cldXYZ = (cld[:, 0:3] - minPt) / resolution
    _fill = minPt[ind] - (maxPt[ind] - minPt[ind])

    img = np.full((div, div), fill_value=_fill, dtype=np.float32)
    for xyz in cldXYZ:
        x = int(xyz[0])
        y = int(xyz[1])
        img[y, x] = xyz[2]
    return img

def proj_img_y_div(cld, div=200):
    ind = 1
    minPt, maxPt = cld_bounding_box(cld)
    resolution = (maxPt - minPt) / (div - 1)
    resolution[ind] = 1
    cldXYZ = (cld[:, 0:3] - minPt) / resolution
    _fill = minPt[ind] - (maxPt[ind] - minPt[ind])

    img = np.full((div, div), fill_value=_fill, dtype=np.float32)
    for xyz in cldXYZ:
        x = int(xyz[0])
        z = int(xyz[2])
        img[z, x] = xyz[1]
    return img