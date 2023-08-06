# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from timeit import default_timer as timer
import time
import copy

import numpy as np
import scipy.interpolate as interp

import pyqtgraph as pg

from PySide2 import QtCore, QtGui, QtWidgets

from . import FloatType, FloatWidget

from .base import VariableWidget
from ..var_tree import VariableTreeItem

from ....base import ( Heading1, Heading2, Heading3, HLine, ToolButton )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SplineXAxis( pg.AxisItem ):
  def tickStrings(self, values, scale, spacing):
    # TODO: make more general to handle different ranges
    return [ "{:.1f}".format(x) for x in values ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SplineYAxis( pg.AxisItem ):
  def tickStrings(self, values, scale, spacing):
    # TODO: make more general to handle different ranges
    return [ "{:.1f}".format(x) for x in values ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SplineViewBox(pg.ViewBox):
  def __init__(self, *args, **kwds):
    super().__init__(*args, **kwds)
    # self.setMouseMode(self.RectMode)

  #----------------------------------------------------------------------------#
  def mouseClickEvent(self, ev):
    if ev.button() == QtCore.Qt.RightButton:
      # add/remove point
      ev.ignore()

  #----------------------------------------------------------------------------#
  def mouseDragEvent(self, ev):
    if ev.button() == QtCore.Qt.RightButton:
      ev.ignore()
    else:
      # move point
      ev.ignore()

  #----------------------------------------------------------------------------#
  def wheelEvent( self, ev ):
    ev.ignore()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PointWidget( QtWidgets.QWidget ):

  #----------------------------------------------------------------------------#
  def __init__ ( self, manager, type, config, spline ):
    super().__init__()

    self._manager = manager

    self._spline = spline

    self.layout = QtWidgets.QHBoxLayout()
    self.setLayout( self.layout )

    xtype = FloatType( label = '', min = type._xmin, max = type._xmax, default = type._xmin )
    ytype = FloatType( label = '', min = type._ymin, max = type._ymax, default = type._ymin )

    self.x = FloatWidget( manager, xtype, config )
    self.y = FloatWidget( manager, ytype, config )

    self.x.changed.connect( self.on_change )
    self.y.changed.connect( self.on_change )

    self.label = QtWidgets.QLabel( "" )

    self.layout.addWidget( self.label )
    self.layout.addWidget( self.x )
    self.layout.addWidget( self.y )

    self.remove_btn = ToolButton(
      self._manager.resource_path('images/icons/remove.svg'),
      "Remove",
      self )

    self.remove_btn.setCursor( QtCore.Qt.PointingHandCursor )

    self.remove_btn.clicked.connect( self.on_remove )

    self.layout.addWidget( self.remove_btn )

    self.add_btn = ToolButton(
      self._manager.resource_path('images/icons/add.svg'),
      "Add",
      self )

    self.add_btn.setCursor( QtCore.Qt.PointingHandCursor )

    self.add_btn.clicked.connect( self.on_add )

    self.layout.addWidget( self.add_btn )

  #----------------------------------------------------------------------------#
  def set_value( self, index, value ):
    self._index = index
    self.label.setText( str(index) )

    self.x.set_value( value[0] )
    self.y.set_value( value[1] )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    return [ self.x.get_value(), self.y.get_value() ]

  #----------------------------------------------------------------------------#
  def can_add( self, flag ):
    self.add_btn.setEnabled( flag )

  #----------------------------------------------------------------------------#
  def can_remove( self, flag ):
    self.remove_btn.setEnabled( flag )

  #----------------------------------------------------------------------------#
  def on_add( self ):
    self._spline.on_add( self._index )

  #----------------------------------------------------------------------------#
  def on_remove( self ):
    self._spline.on_remove( self._index )

  #----------------------------------------------------------------------------#
  def on_change( self ):
    self._spline.on_change()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatSpline2DWidget ( VariableWidget ):

  changed = QtCore.Signal(object)

  #----------------------------------------------------------------------------#
  def __init__ ( self, manager, type, config, tree_parent = None ):
    super().__init__()

    self._manager = manager
    self._type = type
    self._config = config
    self._tree_parent = tree_parent
    self._tree_item = None

    self._points = None

    self.layout = QtWidgets.QVBoxLayout()
    self.setLayout( self.layout )

    self._ax0 = SplineXAxis( orientation='bottom' )
    self._ax1 = SplineYAxis( orientation='left' )
    self._vb = SplineViewBox()

    self._plotw = pg.PlotWidget(
      viewBox = self._vb,
      axisItems = {
        'bottom': self._ax0,
        'left' : self._ax1 },
      enableMenu = False,
      title = None )

    screen = QtGui.QGuiApplication.primaryScreen()
    screenGeometry = screen.geometry()
    width = screenGeometry.width() / 6

    self._plotw.setMinimumSize( width, width )
    self._plotw.setAspectLocked( True )

    self._plotw.setXRange(type._xmin, type._xmax)
    self._plotw.setYRange(type._ymax, type._ymin)

    self._plot_line = self._plotw.plot(
      pen = pg.mkPen(
        width = 1,
        color = '#a8a8a8') )
    # self._plot_line.setPen((200,200,100)) # rgb?

    self._plot_pts = self._plotw.plot(
      pen = None,
      symbol = 'o',
      symbolSize = 12,
      symbolBrush = pg.mkBrush(
        color = '#525252'
      ),
      symbolPen = pg.mkPen(
        color = '#a8a8a8' ) )


    self.layout.addWidget( self._plotw )

    self.layout.addWidget( HLine() )

    self.hlayout = QtWidgets.QHBoxLayout()
    self.layout.addLayout( self.hlayout )

    if type._xname is not None:
      self._plotw.setLabel('bottom', type._xname )
      xcol = Heading3( type._xname )
      xcol.setAlignment( QtCore.Qt.AlignCenter )
      self.hlayout.addWidget( xcol )

    if type._yname is not None:
      self._plotw.setLabel('left', type._yname )
      ycol = Heading3( type._yname )
      ycol.setAlignment( QtCore.Qt.AlignCenter )
      self.hlayout.addWidget( ycol )

    self._pts_widgets = []

    if self._tree_parent is not None:
      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 2, self )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):

    if len(value) < 2:
      value = [ [ 0.0, 0.0 ], [1.0, 1.0] ]

    self._points = copy.deepcopy( value )

    num_pts = len( value )

    rm = self._pts_widgets[ num_pts: ]

    for w in rm:
      self.layout.removeWidget( w )
      w.setParent( None )

    self._pts_widgets = self._pts_widgets[ :num_pts ]

    for i, w in enumerate(self._pts_widgets):
      w.set_value( i, value[i] )

    offset = len( self._pts_widgets )
    mk = value[ offset: ]

    for i, v in enumerate(mk):

      w = PointWidget(
        manager = self._manager,
        type = self._type,
        config = self._config,
        spline = self )

      w.set_value( i + offset, v )
      self._pts_widgets.append( w )
      self.layout.addWidget( w )

    self.plot_poly_fit( self._points )

    can_add = num_pts < self._type._max_pts
    can_remove = num_pts > self._type._min_pts

    self._pts_widgets[0].can_add( can_add )
    self._pts_widgets[0].can_remove( False )

    self._pts_widgets[-1].can_add( False )
    self._pts_widgets[-1].can_remove( False )

    for w in self._pts_widgets[1:-1]:
      w.can_add( can_add )
      w.can_remove( can_remove )

  #----------------------------------------------------------------------------#
  def plot_poly_fit( self, points ):

    px, py = list( zip( *points ) )
    px = np.array( px )
    py = np.array( py )

    poly = interp.CubicSpline(
      x = px,
      y = py,
      bc_type=((2, 0.0), (2, 0.0)) )

    x = np.linspace( 0.0, 1.0, 100 )
    y = poly( x )

    np.clip( y, 0.0, 1.0, out = y )

    self._plot_line.setData(x = x, y = y )
    self._plot_pts.setData(x = px, y = py )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    points = []

    for w in self._pts_widgets:
      points.append( w.get_value() )

    return points

  #----------------------------------------------------------------------------#
  def on_add( self, index ):

    if index >= len( self._points ):
      return

    a = self._points[index]
    b = self._points[index+1]

    c = [ 0.5 * ( a[0] + b[0] ), 0.5 * ( a[1] + b[1] ) ]

    self._points.insert( index + 1, c )

    self.set_value( self._points )

  #----------------------------------------------------------------------------#
  def on_remove( self, index ):

    self._points.pop( index )

    self.set_value( self._points )

  #----------------------------------------------------------------------------#
  def on_change( self ):
    value = self.get_value()
    self.set_value( value )
    self.changed.emit( value )
