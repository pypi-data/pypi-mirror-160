#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/22 17:32:21

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import sys
import logging
import logging.handlers
from pathlib import Path
import os.path
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['get_logger']


def _add_handler_rotate_file(filename, fmt = None):
    handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=1024 * 1024 * 1024 * 1,
        backupCount=5,
    )
    if fmt:
        handler.setFormatter(fmt)
    return handler

def _add_handler_file(filename, fmt = None):
    handler = logging.FileHandler(filename)
    if fmt:
        handler.setFormatter(fmt)
    return handler

def _add_handler_console(fmt = None):
    handler = logging.StreamHandler()
    if fmt:
        handler.setFormatter(fmt)
    return handler

def get_logger(name=None, filename=None, fmt=None, level=None):
    if name is None:
        try:
            name = Path(sys.modules.get('__main__').__file__).stem
        except :
            name = "laok"
    log = logging.getLogger(name)

    if fmt is None:
        fmt = '[%(asctime)s][%(levelname)s]%(message)s'
    fmtter = logging.Formatter(fmt)

    if level is None:
        level = logging.DEBUG
    log.setLevel(level)

    log.addHandler(_add_handler_console(fmtter))

    if filename is not None:
        _, ext = os.path.splitext(filename)
        if not ext:
            filename = filename + ".log"
        log.addHandler(_add_handler_file(filename, fmtter))

    return log

