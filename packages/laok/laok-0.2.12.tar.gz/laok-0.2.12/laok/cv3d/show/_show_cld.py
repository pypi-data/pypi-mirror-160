#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022/5/26 20:52:29

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''

#===============================================================================
'''     
'''
#===============================================================================
__all__ = ['show_cld_xyz', 'VtkWindow']

class VtkWindow:
    def __init__(self):
        import vtk
        ren = vtk.vtkRenderer()
        ren.SetBackground(0, 0, 0)

        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)
        renWin.SetSize(400, 400)
        renWin.SetWindowName('3D viewer')

        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        iren.SetInteractorStyle(vtk.vtkInteractorStyleMultiTouchCamera())

        self.ren_ = ren
        self.renWin_ = renWin
        self.iren_ = iren

    def add_cylinder(self):
        import vtk
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(8)
        mapper.SetInputConnection(cylinder.GetOutputPort())

        self.ren_.AddActor(actor)
        return actor

    def add_xyz(self, array, color=(255,255,255)):
        import vtk
        from vtkmodules.util.numpy_support import numpy_to_vtk

        points = vtk.vtkPoints()
        points.SetData(numpy_to_vtk(array))

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        vertex = vtk.vtkVertexGlyphFilter()
        vertex.SetInputData(polydata)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vertex.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color[0]/255, color[1]/255, color[2]/255)
        self.ren_.AddActor(actor)
        return actor

    def show(self):
        self.iren_.Initialize()
        self.ren_.ResetCamera()
        self.renWin_.Render()
        self.iren_.Start()


def show_cld_xyz(arr, color=(255,255,255)):
    from ._vtk import VtkWin3d
    win = VtkWin3d()
    win.add_xyz(arr, color=color)
    win.show()

