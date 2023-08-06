#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/10 17:51:24

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import requests
#===============================================================================
'''     
'''
#===============================================================================

def download_file(url, save_name):
    with open(save_name, 'wb') as f:
        file = requests.get(url)
        f.write(file.content)

def request_text(url):
    return requests.get(url).text

def request_json(url):
    return requests.get(url).json()

