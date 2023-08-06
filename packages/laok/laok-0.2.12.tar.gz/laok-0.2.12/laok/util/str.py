#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/6/1 15:25:00

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['float_value']


def float_value(val, default=None):
    try:
        return float(val)
    except:
        return default

