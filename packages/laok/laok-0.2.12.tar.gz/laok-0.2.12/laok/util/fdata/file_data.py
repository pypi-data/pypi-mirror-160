#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 21:01:14

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''     
'''
#===============================================================================

__all__ = ['file_read_text', 'file_read_bin', 'file_write_text', 'file_write_bin',
           'file_read_lines']

def file_read_text(fname, encoding=None):
    with open(fname, mode='r', encoding=encoding) as f:
        return f.read()

def file_read_lines(fname, encoding=None, strip = True):
    with open(fname, mode='r', encoding=encoding) as f:
        line = f.readline()
        if strip:
            line = line.strip()
        yield line

def file_read_bin(fname):
    with open(fname, mode='rb') as f:
        return f.read()

def file_write_text(fname, text, encoding=None):
    with open(fname, mode='w', encoding=encoding) as f:
        f.write(text)

def file_write_bin(fname, data):
    with open(fname, mode='wb') as f:
        f.write(data)

