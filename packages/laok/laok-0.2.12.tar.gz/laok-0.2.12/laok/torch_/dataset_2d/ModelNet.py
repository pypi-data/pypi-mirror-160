#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/3/7 15:43:22

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import numpy as np
from torch.utils.data import Dataset
import laok.cv3d as kcv3
import laok.cv2d as kcv2
import cv2
#===============================================================================
# 
#===============================================================================
__all__ = ['ModelNetProjImage']


class ModelNetProjImage(Dataset):
    def __init__(self, root, div=500, split='train', num_category=40, cache_size=30000, transform=None):
        assert (split == 'train' or split == 'test')

        # 加载类别列表
        catfile = os.path.join(root, f'modelnet{num_category}_shape_names.txt')
        with open(catfile) as f:
            self.classes = {line.rstrip(): i for i, line in enumerate(f)}
        print(f'classes : {self.classes}')

        # 加载数据文件列表
        shape_name_file = f'modelnet{num_category}_{split}.txt'
        print(f'{split} file : {shape_name_file}')
        with open(os.path.join(root, shape_name_file))as f:
            shape_ids = [line.rstrip() for line in f]
        shape_names = ['_'.join(x.split('_')[0:-1]) for x in shape_ids]  # 去除尾数
        # list of (shape_name, shape_txt_file_path) tuple
        self.datapath = [(shape_names[i], os.path.join(root, shape_names[i], shape_ids[i])) for i
                         in range(len(shape_ids))]
        print(f'The size of {split} data is {len(self.datapath)}')
        self.div = div
        self._cache = {}
        self.cache_size = cache_size
        self.transform = transform

    def __len__(self):
        return len(self.datapath)

    def __getitem__(self, index):
        if index in self._cache:
            return self._cache[index]

        name, dfile = self.datapath[index]
        cls = self.classes[name]
        cls = np.array([cls]).astype(np.int32)

        cld = kcv3.load_cld_xyz(dfile + ".txt", delimiter=',')
        img_x = kcv3.proj_img_x_div(cld, self.div)
        img_y = kcv3.proj_img_y_div(cld, self.div)
        img_z = kcv3.proj_img_z_div(cld, self.div)

        img_x = kcv2.normlize_uint8(img_x)
        img_y = kcv2.normlize_uint8(img_y)
        img_z = kcv2.normlize_uint8(img_z)

        img_list = [img_x, img_y, img_z]
        img = cv2.merge(img_list)

        if self.transform:
            img = self.transform(img)

        if index < self.cache_size:
            self._cache[index] = (img, cls)
        return img, cls