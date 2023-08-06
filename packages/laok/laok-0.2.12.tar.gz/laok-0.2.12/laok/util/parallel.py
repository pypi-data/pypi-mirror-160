#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/19 13:51:55

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import threading
import concurrent.futures as futures
from .fpath import (files_under as _files_under,
                    files_current as _files_current,
                    dirs_current as _dirs_current,
                    dirs_under as _dirs_under)
#===============================================================================
'''     
'''
#===============================================================================

####################    线城接口
def thread_id():
    return threading.get_ident()

def thread_count():
    return threading.active_count()

####################    并行接口
def parallel_sequence(data_list, handler, max_workers=None, use_thread = True):
    if use_thread:
        Executor = futures.ThreadPoolExecutor
    else:
        Executor = futures.ProcessPoolExecutor

    with Executor(max_workers=max_workers) as ex:
        wait_for = [ex.submit(handler, data) for data in data_list]
        return [f.result() for f in futures.as_completed(wait_for)]

def files_under(dir_name, handler, suffix_list = None, need_join_dir=True, max_workers=None, use_thread = True):
    '''
    '''
    data_iter = _files_under(dir_name, suffix_list, need_join_dir)
    return parallel_sequence(data_iter, handler, max_workers=max_workers, use_thread=use_thread)

def files_current(dir_name, handler, suffix_list = None, need_join_dir=True, max_workers=None, use_thread = True):
    '''
    '''
    data_iter = _files_current(dir_name, suffix_list, need_join_dir)
    return parallel_sequence(data_iter, handler, max_workers=max_workers, use_thread=use_thread)

def dirs_under(dir_name, handler, suffix_list = None, need_join_dir=True, max_workers=None, use_thread = True):
    '''
    '''
    data_iter = _dirs_under(dir_name, suffix_list, need_join_dir)
    return parallel_sequence(data_iter, handler, max_workers=max_workers, use_thread=use_thread)

def dirs_current(dir_name, handler, suffix_list = None, need_join_dir=True, max_workers=None, use_thread = True):
    '''
    '''
    data_iter = _dirs_current(dir_name, suffix_list, need_join_dir)
    return parallel_sequence(data_iter, handler, max_workers=max_workers, use_thread=use_thread)


