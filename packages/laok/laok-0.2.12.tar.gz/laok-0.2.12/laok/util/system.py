#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 15:41:47

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import platform, sys
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['is_linux', 'is_windows', ]


def is_windows():
    return platform.system().lower() == 'windows'

def is_linux():
    return platform.system().lower() == 'linux'

def line_num(depth = 1):
    '''获取当前行号
    '''
    return sys._getframe(depth).f_lineno

def func_name(depth = 1):
    '''获取当前函数名字
    '''
    return sys._getframe(depth).f_code.co_name
