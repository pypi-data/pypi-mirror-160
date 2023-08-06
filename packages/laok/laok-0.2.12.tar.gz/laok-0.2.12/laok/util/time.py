#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/17 21:11:08

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import time as _time
import sys
from contextlib import contextmanager as _context
from functools import wraps as _wraps
from collections import OrderedDict as _OrderedDict
from datetime import datetime
#===============================================================================
# 
#===============================================================================
__all__ = ['datetime_str', 'auto_timer', 'Timer',  'deco_time', 'TimerLabel']

def datetime_str(fmt='%Y%m%d%H%M%S', dt = None):
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y%m%d%H%M%S')

@_context
def auto_timer(msg = '', need_print = True):
    t1 = _time.time()
    yield
    t2 = _time.time()
    if need_print:
        print(f'{msg} [time:{(t2-t1)*1000}(ms)]')

def deco_time(stream = None):
    '''
    装饰器,记录时间
    '''
    def _w1(func):
        @_wraps(func)
        def _w2(*args, **kwargs):
            start = _time.time()
            res = func(*args, **kwargs)
            stop = _time.time()
            if _time is None:
                stream = sys.stdout
            stream.write(f"[{ func.__name__ }] use time [{ 1000*(stop-start) }(ms)]\n")
            return res
        return _w2
    return _w1

class Timer:
    def __init__(self):
        self.restart()

    def restart(self):
        self._t1 = _time.time()

    def elapse(self):
        '''
        time in seconds since the Epoch
        :return:
        '''
        return _time.time() - self._t1


class TimerLabel:
    def __init__(self):
        self._t1 = _OrderedDict()
        self._t2 = _OrderedDict()
        self._enabled = True
        self._total_count = None
        self._cur_count = 0

    def setEnabled(self, val):
        self._enabled = val

    def setReportCount(self, cnt):
        self._total_count = cnt
        self._cur_count = 0

    def start(self, name):
        if self._enabled:
            self._t1[name] = _time.time()

    def end(self, name):
        if self._enabled:
            self._t2[name] = _time.time()            

    def report(self, stream = None):
        if not self._enabled:
            return 
        
        if self._total_count is not None:
            if self._cur_count > self._total_count:
                return
            self._cur_count += 1

        if stream is None:
            stream = sys.stdout
        
        curt = _time.time()
        stream.write("\n***** time summary *****\n")
        for name,t1 in self._t1.items():
            t2 = self._t2.get(name, curt)
            stream.write(f'"{name}" time use: {t2-t1}(s)\n')


if __name__ == "__main__":
    import math
    a = 0
    with auto_timer() as t:
        for i in range(1,10000000):
            a += math.cos(1)

    times = TimerLabel()
    times.setReportCount(2)

    for i in range(5):
        times.start('it1')
        _time.sleep(1)
        times.start('it2')
        _time.sleep(3)
        times.report()