#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/3/7 17:34:59

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import numpy as np
#===============================================================================
#
#===============================================================================
__all__ = ['load_cld_xyz']

def load_cld_xyz(fname, delimiter=None):
    return np.loadtxt(fname, delimiter=delimiter)

