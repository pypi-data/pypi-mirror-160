#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 08:58:19

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import torch
from .base import save_model_params, load_model_params
from laok.util.time import datetime_str
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['ModelCheckPoint']

def _split_file_name(filename):
    try:
        fname = os.path.split(filename)[1]
        basename = os.path.splitext(fname)[0]
        value = basename.split('-')[-1]
        value = float(value)
    except Exception as e:
        value = None

    return fname, value

def _save_file_name(model_path, name, value):
    dt = datetime_str()
    _save_file = os.path.join(model_path, f'{name}-{dt}-{value:.4f}.pt')
    return _save_file

class ModelCheckPoint:
    '''automatically load or save the current best model
    '''
    def __init__(self, model, model_save_path='./model_save/', name='model', keep_best=True, show_info=True):
        self.model_ = model
        self.model_save_path_ = model_save_path
        self.name_ = name
        self.value_ = None
        self.show_info_ = show_info
        self.keep_best_ = keep_best
        if not os.path.exists(model_save_path):
            os.makedirs(model_save_path)

    def update(self, value):
        '''the model needs to be saved according to the value
        '''
        _save_file = None

        # check if need save model
        if self.value_ is None or self.value_ < value:
            self.value_ = value  # update the best value
            _save_file = _save_file_name(self.model_save_path_, name=self.name_, value = value)
            save_model_params(self.model_, _save_file)
            if self.show_info_:
                print(f'save checkpoint {_save_file}')

        if self.show_info_:
            if self.value_ == value:
                print(f"current {self.name_} value is {value:.4f}, it's the best.!!!")
            else:
                print(f'current {self.name_} value is {value:.4f}, while the best value is {self.value_:.4f}')

        # load the best one model from model path
        if self.keep_best_:
            self.load_from_path()

        return _save_file

    def load_from_path(self, ext=".pt"):
        max_value = None
        max_value_file = None

        for fname in os.listdir(self.model_save_path_):
            if not fname.endswith(ext):
                continue

            _fname, _value = _split_file_name(fname)

            # print(_fname, _value)
            if max_value is None or max_value < _value:
                max_value = _value
                max_value_file = _fname

        if max_value_file and max_value and (self.value_ is None or max_value > self.value_):
            self.value_ = max_value
            _load_file = os.path.join(self.model_save_path_, max_value_file)
            load_model_params(_load_file, self.model_)
            if self.show_info_:
                # if _dist.is_initialized():
                #     print(f'rank[{_dist.get_rank()}], load checkpoint: {_load_file}, value:{self._value}')
                # else:
                print(f'load checkpoint: {_load_file}, value:{self.value_}')

        return max_value, max_value_file

    def load_from_file(self, model_file, value=None):
        _fname, _value = _split_file_name(model_file)
        _dir = os.path.split(model_file)[0]

        if os.path.abspath(_dir) == os.path.abspath(self.model_save_path_):
            self.value_ = _value if value is None else value

        load_model_params(model_file, self.model_)
        if self.show_info_:
            # if _dist.is_initialized():
            #     print(f'rank[{_dist.get_rank()}], load model file: {model_file}, value:{self._value}')
            # else:
            print(f'load model file: {model_file}, value:{self.value_}')
