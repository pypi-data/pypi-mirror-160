#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/14 16:47:51

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
from collections import OrderedDict
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['ClsIdx']

class ClsIdx:
    def __init__(self, cls_file = None):
        self.cls_data_ = OrderedDict()
        if cls_file:
            self.setClsFile(cls_file)

    def setClsFile(self, cls_file):
        with open(cls_file) as f:
            for i,line in enumerate(f):
                self.cls_data_[i] = line.strip()
        return self

    def getName(self, idx):
        _idx = int(idx)
        return self.cls_data_.get(_idx, '')

    def getIndex(self, name):
        if name == None or name == '':
            return -1
        for _idx, _name in self.cls_data_.items():
            if name in _name:
                return _idx
        return -1

    def show(self):
        for k,v in self.cls_data_.items():
            print(f'{k}={v}')
