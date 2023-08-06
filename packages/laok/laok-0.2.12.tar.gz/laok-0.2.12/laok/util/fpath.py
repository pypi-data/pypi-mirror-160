#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/27 14:18:09

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import os.path as opath
from pathlib import Path
import shutil
from contextlib import contextmanager
#===============================================================================
# 
#===============================================================================

@contextmanager
def scope_work_dir(dir):
    try:
        old_dir = os.getcwd()
        yield os.chdir(dir)
    finally:
        os.chdir(old_dir)

def path_native(fpath):
    return opath.normpath(fpath).replace('\\', '/').replace('/', os.sep)

def path_unix(fpath):
    return opath.normpath(fpath).replace('\\', '/')

def path_win(fpath):
    return opath.normpath(fpath).replace('/', '\\')

def path_rel(fpath, parent):
    return path_unix(os.path.relpath(fpath, parent))

def files_env(key, filename):
    for pth in os.getenv(key).split(';'):
        full_path = opath.join(pth, filename)
        if opath.exists(full_path):
            yield path_unix(full_path)

def file_env(key, filename):
    for pth in os.getenv('path').split(';'):
        full_path = opath.join(pth, filename)
        if opath.exists(full_path):
            return path_unix(full_path)

def path_exe_file(filename):
    if opath.exists(filename):
        return path_unix(filename)
    return file_env('path', filename)

def path_exe_files(filename):
    if opath.exists(filename):
        yield path_unix(filename)
    for full_path in files_env('path', filename):
        yield path_unix(full_path)

def path_parent(fpath):
    '''fpath: 输入路径名字
       ret: 返回父路径
    '''
    return path_unix(opath.split(fpath)[0])

def path_make_parent(fpath):
    parent = path_parent(fpath)
    os.makedirs(parent, exist_ok=True)
    return parent

def path_make(fpath):
    os.makedirs(fpath, exist_ok=True)

def path_join(*args, make_parent=False):
    fpath = os.path.join(*args)
    if make_parent:
        path_make_parent(fpath)
    return path_unix(fpath)

def path_abs(fpath):
    return path_unix(os.path.abspath(fpath))

def path_exist(fpath):
    return fpath and os.path.exists(fpath)

def file_size(fpath):
    return os.path.getsize(fpath)

def file_delete(fpath):
    os.remove(fpath)

def dir_delete(dirpath):
    shutil.rmtree(dirpath)

def path_is_file(fpath):
    return fpath and os.path.isfile(fpath)

def path_is_dir(fpath):
    return fpath and os.path.isdir(fpath)

def path_filename(fpath, level=0):
    '''fpath: 输入路径名字
       ret: 返回文件名字
    '''
    splits = Path(fpath).splitall()
    return opath.split(fpath)[1]

def path_basename(fpath):
    '''file_path: 输入路径名字
       ret: 返回去掉后缀的文件名字
    '''
    return os.path.basename(fpath)

def path_sterm(fpath):
    return Path(fpath).stem

def path_ext(fpath, need_dot = True):
    '''file_path: 输入路径名字
       ret: 返回后缀
    '''
    fname = opath.split(fpath)[1]
    ext = opath.splitext(fname)[1]
    if ext and not need_dot:
        return ext[1:]
    return ext

def path_replace_ext(file_path, ext):
    '''file_path: 输入路径名字
       ext: 需要替换的后缀名字
       ret: 返回替换后的路径
    '''
    if isinstance(ext, str) and not ext.startswith('.'):
        ext = '.' + ext
    new_file = opath.splitext(file_path)[0] + ext
    return path_unix(new_file)

def path_replace_stem(file_path, basename):
    '''
        file_path：输入路径名字
        basename: 替换的文件名字,保留后缀
        ret: 返回替换后的路径
    '''
    _dir, _fname = opath.split(file_path)
    _basename, _ext = opath.splitext(_fname)
    return path_unix(opath.join(_dir, basename + _ext))

def path_replace_basename(file_path, filename):
    '''
        file_path：输入路径名字
        filename: 替换的文件名字
        ret: 返回替换后的路径
    '''
    _dir, _fname = opath.split(file_path)
    return path_unix(opath.join(_dir, filename))

def path_replace_parent(file_path, parent):
    '''
        file_path：输入路径名字
        parent: 替换的父路径
        ret: 返回替换后的路径
    '''
    _dir, _fname = opath.split(file_path)
    return path_unix(opath.join(parent, _fname))

def _ensure_list(suffix_list):
    if suffix_list is None:
        return []
    if isinstance(suffix_list, list):
        return suffix_list
    if isinstance(suffix_list, str):
        return suffix_list.split(';')
    return suffix_list

def _file_name_endswith(fname, suffix_list):
    return suffix_list and any( (fname.lower().endswith(s.lower()) for s in suffix_list) )

def files_under(dir_name, suffix_list = None, need_join_dir=True):
    '''
    dir_name: 路径
    suffix_list: 后缀列表, 比如: [.txt,.py];用于筛选文件
    ret: 返回生成器
    '''
    suffix_list = _ensure_list(suffix_list)
    for fdir_name, _sub_fdirs, files in os.walk(dir_name):
        for fname in files:
            if not suffix_list or _file_name_endswith(fname, suffix_list):
                yield path_unix(os.path.join(fdir_name, fname) if need_join_dir else fname)

def files_current(dir_name, suffix_list = None, need_join_dir=True):
    '''
    dir_name: 路径
    suffix_list: 后缀列表, 比如: [.txt,.py];用于筛选文件
    ret: 返回生成器
    '''
    suffix_list = _ensure_list(suffix_list)
    for fname in os.listdir(dir_name):
        fpath = os.path.join(dir_name, fname)
        if os.path.isfile(fpath):
            if not suffix_list or _file_name_endswith(fname, suffix_list):
                yield path_unix(fpath if need_join_dir else fname)

def dirs_under(dir_name, suffix_list = None, need_join_dir=True):
    '''
    dir_name: 路径
    suffix_list: 后缀列表, 比如: [.txt,.py]
    ret: 返回生成器
    '''
    suffix_list = _ensure_list(suffix_list)
    for fdir_name, sub_fdirs, files in os.walk(dir_name):
        for fname in sub_fdirs:
            if not suffix_list or _file_name_endswith(fname, suffix_list):
                yield path_unix(os.path.join(fdir_name, fname) if need_join_dir else fname)

def dirs_current(dir_name, suffix_list = None, need_join_dir=True):
    '''
    dir_name: 路径
    suffix_list: 后缀列表, 比如: [test, test2];用于筛选路径
    ret: 返回生成器
    '''
    suffix_list = _ensure_list(suffix_list)
    for fname in os.listdir(dir_name):
        fpath = os.path.join(dir_name, fname)
        if os.path.isdir(fpath):
            if not suffix_list or _file_name_endswith(fname, suffix_list):
                yield path_unix(fpath if need_join_dir else fname)

