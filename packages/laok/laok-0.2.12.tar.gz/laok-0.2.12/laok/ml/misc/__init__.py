#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 12:16:18

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import numpy as np
import random
#===============================================================================
'''     
'''
#===============================================================================

__all__ = ['print2', 'init_seeds']

def print2(data, name = None):
    '''print detail data information
    '''
    msg = f"==== name:{name} " if name else "=== "
    msg += f'id:{id(data)} type:{type(data)}\n'

    if isinstance(data, np.ndarray):
        msg += f'    shape:{data.shape}\n' \
               f'    dtype:{data.dtype}\n'

    if isinstance(data, np.dtype):
        if data.names:
            msg += f'    names:{data.names}\n'

        if data.shape:
            msg += f'    shape:{data.shape}\n'
            msg += f'    dim:{data.dim}\n'

        if data.hasobject:
            msg += f'    hasobject:{data.hasobject}\n'


        msg += f'    itemsize:{data.itemsize}\n' \
               f'    alignment:{data.alignment}\n' \
               f'    str:{data.str}\n' \
               f'    byteorder:{data.byteorder}\n'

    msg += f'{data}'
    print(msg)


def init_seeds(seed=0):
    # Initialize random number generator (RNG) seeds
    random.seed(seed)
    np.random.seed(seed)
