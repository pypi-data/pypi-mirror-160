#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/3/7 15:43:22

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
# import json
# import torch
# import random
import numpy as np
from torch.utils.data import Dataset
from laok.cv3d.trans import farthest_point_sample, pc_normalize
# import laok.cv2d as kcv2
# import cv2
#===============================================================================
# 
#===============================================================================
__all__ = ['ModelNetNormalResampled']

class ModelNetNormalResampled(Dataset):
    def __init__(self, root, npoint=1024, split='train', num_category=40, uniform=False, normal_channel=True, cache_size=1):
        assert (split == 'train' or split == 'test')
        self.root = root
        self.npoints = npoint
        self.uniform = uniform
        self.normal_channel = normal_channel

        # 加载类别列表
        catfile = os.path.join(self.root, f'modelnet{num_category}_shape_names.txt')
        with open(catfile) as f:
            self.classes = {line.rstrip():i for i,line in enumerate(f)}
        print(f'classes : {self.classes}')

        # 加载数据文件列表
        shape_name_file = f'modelnet{num_category}_{split}.txt'
        print(f'{split} file : {shape_name_file}')
        with open(os.path.join(self.root, shape_name_file) )as f:
            shape_ids = [line.rstrip() for line in f]
        shape_names = ['_'.join(x.split('_')[0:-1]) for x in shape_ids] #去除尾数
        # list of (shape_name, shape_txt_file_path) tuple
        self.datapath = [(shape_names[i], os.path.join(self.root, shape_names[i], shape_ids[i]) + '.txt') for i
                         in range(len(shape_ids))]
        print(f'The size of {split} data is {len(self.datapath)}')

        self.cache_size = cache_size  # how many data points to cache in memory
        self.cache = {}  # from index to (point_set, cls) tuple

    def __len__(self):
        return len(self.datapath)

    def __getitem__(self, index):
        if index in self.cache:
            point_set, cls = self.cache[index]
        else:
            name, dfile = self.datapath[index]
            cls = self.classes[name]
            cls = np.array([cls]).astype(np.int32)
            point_set = np.loadtxt(dfile, delimiter=',').astype(np.float32)

            if self.uniform:
                point_set = farthest_point_sample(point_set, self.npoints)
            else:
                point_set = point_set[0:self.npoints,:]

            point_set[:, 0:3] = pc_normalize(point_set[:, 0:3])

            if not self.normal_channel:
                point_set = point_set[:, 0:3]

            if len(self.cache) < self.cache_size:
                self.cache[index] = (point_set, cls)

        return point_set, cls

