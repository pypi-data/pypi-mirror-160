#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 21:41:00

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['iter_multi']

def iter_multi(seq, cnt=1, drop_last=False):
    data_list = []
    for i,v in enumerate(seq):
        data_list.append(v)
        if len(data_list) == cnt:
            yield data_list
            data_list.clear()

    if not drop_last and len(data_list) > 0:
        yield data_list

# def iter_step(seq, step):
#     data_list = []
#     for i,v in enumerate(seq):
#         data_list.append(v)
#         if len(data_list) == cnt:
#             yield data_list
#             data_list.clear()
#
#     if not drop_last and len(data_list) > 0:
#         yield data_list