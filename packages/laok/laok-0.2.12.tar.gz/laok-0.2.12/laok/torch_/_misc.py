#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/4/20 20:59:02

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch
#===============================================================================
'''     
'''
#===============================================================================
def print2(data, desc = None):
    '''show more data detail
    :param data:
    :return:
    '''
    if torch.is_tensor(data):
        if desc:
            print(f'===== torch.Tensor {desc}')
        else:
            print(f'===== torch.Tensor')
        print(f'type:{data.type()}')
        print(f'size:{data.size()}')
        print(f'dim:{data.dim()}')
        print(data)
    else:
        print(data)

def print_version():
    print(f'torch.__version__:{torch.__version__}')
    print(f'torch.version.cuda:{torch.version.cuda}')
    print(f'torch.backends.cudnn.version():{torch.backends.cudnn.version()}')
    print(f'torch.cuda.get_device_name():{torch.cuda.get_device_name()}')

def print_info():
    print_version()
    print(f'torch.get_default_dtype():{torch.get_default_dtype()}')

    print(f'torch.compiled_with_cxx11_abi():{torch.compiled_with_cxx11_abi()}')
    print(f'torch.is_warn_always_enabled():{torch.is_warn_always_enabled()}')
    print(f'torch.are_deterministic_algorithms_enabled():{torch.are_deterministic_algorithms_enabled()}')
    print(f'torch.is_deterministic_algorithms_warn_only_enabled():{torch.is_deterministic_algorithms_warn_only_enabled()}')


def get_device(idx = 0):
    '''get the suitable device
    :param idx:
    :return:
    '''
    return torch.device(f"cuda:{idx}" if torch.cuda.is_available() else "cpu")

def init_seeds(seed=0):
    '''make the torch enviroment no random.
    '''

    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # # Speed-reproducibility tradeoff https://pytorch.org/docs/stable/notes/randomness.html
    # if seed == 0:  # slower, more reproducible
    #     torch.cudnn.benchmark, torch.cudnn.deterministic = False, True
    # else:  # faster, less reproducible
    #     torch.cudnn.benchmark, torch.cudnn.deterministic = True, False

def cuda_visible_devices(device : str):
    ''' input device str list like: '0,1'
    or usage in command:
        CUDA_VISIBLE_DEVICES=0,1 python train.py
    :param device:
    :return:
    '''
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = str(device)

