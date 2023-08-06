#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 08:58:48

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['save_jit_model', 'save_onnx_model', 'save_model', 'save_model_params',
           'load_model_params', 'load_jit_model'
           ]

def save_jit_model(model, filename, input = None):
    '''save trace model,use eval model to get trace model;
    '''
    if isinstance(model, torch.jit.TracedModule):
        traced_model = model
    else:
        try:
            mode = model.training
            model.eval()
            traced_model = torch.jit.trace(model, input)
        finally:
            model.train(mode)

    traced_model.save(filename)
    return traced_model

def load_jit_model(filename):
    ''' load trace model
    '''
    return torch.jit.load(filename)

def save_onnx_model(model, filename, input = None, **kws):
    '''export model to onnx
    :param model:
    :param filename:
    :param input:
    :return:
    '''
    torch.onnx.export(model, input, filename, **kws)

def save_model(model, filename):
    return torch.save(model, filename)

def save_model_params(model, filename):
    return torch.save(model.state_dict(), filename)

def load_model(filename, map_location=None):
    return torch.load(filename, map_location=map_location)

def load_model_params(filename, model, map_location=None):
    _obj = load_model(filename, map_location=map_location)
    if isinstance(_obj, torch.nn.Module):
        state = _obj.state_dict()
    else:
        state = _obj

    # 加载匹配的部分
    _model_state = model.state_dict()
    part_load = {}
    for k,v in state.items():
        if k in _model_state and _model_state[k].shape == v.shape:
            part_load[k] = v
    _model_state.update(part_load)
    model.load_state_dict(_model_state)
    return model


