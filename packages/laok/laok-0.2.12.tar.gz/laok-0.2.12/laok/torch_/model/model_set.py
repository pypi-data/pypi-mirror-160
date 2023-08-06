#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/20 09:56:07

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
from collections import OrderedDict
import inspect
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['ModelClassSet', 'ModelDetectSet', 'ModelSegmentSet', 'model_class_set']


class ModelSet:
    '''基本的仓库
    '''
    def __init__(self):
        self.model_cls_set_ = OrderedDict()

    def createModel(self, name, **kws):
        return self.model_cls_set_[name](**kws)

    def __iter__(self):
        return iter(self.model_cls_set_.keys())

    def __len__(self):
        return len(self.model_cls_set_)

    def __contains__(self, item):
        return item in self.model_cls_set_

    def __getitem__(self, item):
        return self.model_cls_set_[item]

    def addModelCreator(self, creator, name = None):
        if name is None:
            name = creator.__name__
        if name in self.model_cls_set_:
            raise RuntimeError(f"Already exists: {name}")
        self.model_cls_set_[name] = creator

    def show(self):
        for k,v in self.model_cls_set_.items():
            print(f'{k}={v}')

class ModelClassSet(ModelSet):
    ''' 识别模型的仓库
    '''
    def __init__(self):
        super(ModelClassSet, self).__init__()

        import torchvision.models as m
        model_cls_list = [
            m.alexnet,
            m.convnext_tiny, m.convnext_small, m.convnext_base, m.convnext_large,
            m.densenet121, m.densenet169, m.densenet201, m.densenet161,
            m.efficientnet_b0, m.efficientnet_b1, m.efficientnet_b2, m.efficientnet_b3, m.efficientnet_b4, m.efficientnet_b5, m.efficientnet_b6, m.efficientnet_b7,
            m.googlenet,
            m.inception_v3,
            m.mnasnet0_5, m.mnasnet0_75, m.mnasnet1_0, m.mnasnet1_3,
            m.mobilenet_v2, m.mobilenet_v3_large, m.mobilenet_v3_small,
            m.regnet_y_400mf,m.regnet_y_800mf,m.regnet_y_1_6gf,m.regnet_y_3_2gf,m.regnet_y_8gf,m.regnet_y_16gf,m.regnet_y_32gf,m.regnet_y_128gf,m.regnet_x_400mf,m.regnet_x_800mf,m.regnet_x_1_6gf,m.regnet_x_3_2gf,m.regnet_x_8gf,m.regnet_x_16gf,m.regnet_x_32gf,
            m.resnet18, m.resnet34, m.resnet50, m.resnet101, m.resnet152, m.resnext50_32x4d, m.resnext101_32x8d, m.wide_resnet50_2, m.wide_resnet101_2,
            m.shufflenet_v2_x0_5, m.shufflenet_v2_x1_0, m.shufflenet_v2_x1_5, m.shufflenet_v2_x2_0,
            m.squeezenet1_0, m.squeezenet1_1,
            m.vgg11, m.vgg11_bn, m.vgg13, m.vgg13_bn, m.vgg16, m.vgg16_bn, m.vgg19_bn, m.vgg19,
            m.vit_b_16, m.vit_b_32, m.vit_l_16, m.vit_l_32,
        ]
        for model_cls in model_cls_list:
            self.addModelCreator(model_cls)

class ModelDetectSet(ModelSet):
    '''检测模型仓库
    '''
    def __init__(self):
        super(ModelDetectSet, self).__init__()

        import torchvision.models.detection as m
        model_cls_list = [
            m.fasterrcnn_resnet50_fpn, m.fasterrcnn_mobilenet_v3_large_320_fpn, m.fasterrcnn_mobilenet_v3_large_fpn,
            m.fcos_resnet50_fpn,
            m.keypointrcnn_resnet50_fpn,
            m.maskrcnn_resnet50_fpn,
            m.retinanet_resnet50_fpn,
            m.ssd300_vgg16,
            m.ssdlite320_mobilenet_v3_large,
        ]
        for model_cls in model_cls_list:
            self.addModelCreator(model_cls)

    def createModel(self, name, **kws):
        func = self.model_cls_set_[name]
        if 'pretrained_backbone' in inspect.getcallargs(func):
            kws['pretrained_backbone'] = kws.pop('pretrained_backbone', False)
        return func(**kws)

class ModelSegmentSet(ModelSet):
    '''检测模型仓库
    '''
    def __init__(self):
        super(ModelSegmentSet, self).__init__()

        import torchvision.models.segmentation as m
        model_cls_list = [
            m.deeplabv3_resnet50, m.deeplabv3_resnet101, m.deeplabv3_mobilenet_v3_large,
            m.fcn_resnet50, m.fcn_resnet101,
            m.lraspp_mobilenet_v3_large,
        ]
        for model_cls in model_cls_list:
            self.addModelCreator(model_cls)

    def createModel(self, name, **kws):
        func = self.model_cls_set_[name]
        if 'pretrained_backbone' in inspect.getcallargs(func):
            kws['pretrained_backbone'] = kws.pop('pretrained_backbone', False)
        return func(**kws)


model_class_set = ModelClassSet()

