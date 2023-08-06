#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 16:05:32

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch
#===============================================================================
'''     
'''
#===============================================================================
def torch_to_numpy(t):
    return t.numpy()

def numpy_to_torch(arr):
    return torch.from_numpy(arr)
