#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/12 19:01:15

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''  从 qudida 引用的 变换方法
'''
#===============================================================================
__all__ = ['DomainAdapter']

class DomainAdapter:
    def __init__(self, ref_img, n_components=1, color_conversions=(None, None)):
        from sklearn.decomposition import PCA
        from qudida import DomainAdapter as _Alg
        self._alg = _Alg(transformer=PCA(n_components=n_components), ref_img=ref_img, color_conversions=color_conversions)

    def __call__(self, image):
        return  self._alg(image)


