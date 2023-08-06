#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/12 21:33:43

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import matplotlib.pyplot as plt
#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['draw_bar', 'draw_fill_between', 'draw_plot', 'draw_scatter', 'draw_stem', 'draw_step',
            'draw_boxplot', 'draw_errorbar', 'draw_eventplot', 'draw_hexbin', 'draw_hist',
            'draw_hist2d', 'draw_pie', 'draw_violinplot', 'draw_barbs', 'draw_contour',
            'draw_contourf', 'draw_imshow', 'draw_pcolormesh', 'draw_quiver', 'draw_streamplot',
            'draw_tricontour', 'draw_tricontourf', 'draw_tripcolor', 'draw_triplot'
           ]
################### basic

def _get_kws(d):
    d = d.copy()
    d.pop('kwargs')
    for k in list(d.keys()):
        if d[k] is None:
            d.pop(k)
    return d

def draw_bar(x, height, width=0.8, bottom=None, align="center",
             color=None, edgecolor=None, linewidth=None, tick_label=None,
             xerr=None, yerr=None, ecolor=None, capsize=None, error_kw=None, log=None,
             **kwargs):
    plt.bar(**_get_kws(locals()))

def draw_barh(*args, **kwargs):
    return plt.barh(*args, **kwargs)

def draw_fill_between(*args, **kwargs):
    return plt.fill_between(*args, **kwargs)

def draw_plot(*args, **kwargs):
    return plt.plot(*args, **kwargs)

def draw_scatter(*args, **kwargs):
    return plt.scatter(*args, **kwargs)

def draw_stem(*args, **kwargs):
    return plt.stem(*args, **kwargs)

def draw_step(*args, **kwargs):
    return plt.step(*args, **kwargs)

################### stats
def draw_boxplot(*args, **kwargs):
    return plt.boxplot(*args, **kwargs)

def draw_errorbar(*args, **kwargs):
    return plt.errorbar(*args, **kwargs)

def draw_eventplot(*args, **kwargs):
    return plt.eventplot(*args, **kwargs)

def draw_hexbin(*args, **kwargs):
    return plt.hexbin(*args, **kwargs)

def draw_hist(*args, **kwargs):
    return plt.hist(*args, **kwargs)

def draw_hist2d(*args, **kwargs):
    return plt.hist2d(*args, **kwargs)

def draw_pie(*args, **kwargs):
    return plt.pie(*args, **kwargs)

def draw_violinplot(*args, **kwargs):
    return plt.violinplot(*args, **kwargs)

################### arrays
def draw_barbs(X,Y,U,V, pivot='tip', length=7, barbcolor=None, flagcolor=None,
                 sizes=None, fill_empty=False, barb_increments=None,
                 rounding=True, flip_barb=False, **kws):
    plt.barbs(X,Y,U,V, pivot=pivot, length=length, barbcolor=barbcolor, flagcolor=flagcolor,
                sizes=sizes, fill_empty=fill_empty, barb_increments=barb_increments,
                rounding=rounding, flip_barb=flip_barb, **kws)

def draw_contour(*args, **kwargs):
    return plt.contour(*args, **kwargs)

def draw_contourf(*args, **kwargs):
    return plt.contourf(*args, **kwargs)

def draw_imshow(*args, **kwargs):
    return plt.imshow(*args, **kwargs)

def draw_pcolormesh(*args, **kwargs):
    return plt.pcolormesh(*args, **kwargs)

def draw_quiver(*args, **kwargs):
    return plt.quiver(*args, **kwargs)

def draw_streamplot(*args, **kwargs):
    return plt.streamplot(*args, **kwargs)

################### unstructured

def draw_tricontour(*args, **kwargs):
    return plt.tricontour(*args, **kwargs)

def draw_tricontourf(*args, **kwargs):
    return plt.tricontourf(*args, **kwargs)

def draw_tripcolor(*args, **kwargs):
    return plt.tripcolor(*args, **kwargs)

def draw_triplot(*args, **kwargs):
    return plt.triplot(*args, **kwargs)
