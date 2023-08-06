#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/12 21:23:44

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import matplotlib.pyplot as plt
import numpy as np
#===============================================================================
'''     
'''
#===============================================================================

__all__ = ['draw_data_clusters',
           ]

def draw_data_clusters(X, labels, index_list=(0, 1)):
    clusters = np.unique(labels)
    x, y = index_list
    for cluster in clusters:
        row_ix = np.where(labels == cluster)
        plt.scatter(X[row_ix, x], X[row_ix, y])

