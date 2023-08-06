# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import trio
import time
import logging
log = logging.getLogger( __name__ )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.utils.async_trio import (
  AsyncTarget )

from partis.utils import (
  ModelHint )

from .base import (
  ToolButton )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class Crumb( QtWidgets.QLabel, QtWidgets.QWidget ):
class Crumb( QtWidgets.QWidget ):

  pop_from = QtCore.Signal(int)

  #----------------------------------------------------------------------------#
  def __init__( self, idx, text ):
    super().__init__()

    self._hlayout = QtWidgets.QHBoxLayout(self)
    self._hlayout.setSpacing(0)
    self._hlayout.setContentsMargins(0,0,0,0)

    self.setLayout(self._hlayout)

    if idx >= 1:
      self._hlayout.addWidget( QtWidgets.QLabel(" / ") )

    self._pop_btn = QtWidgets.QToolButton()
    self._pop_btn.setText(text)
    self._pop_btn.clicked.connect( self.on_pop )

    self._hlayout.addWidget( self._pop_btn )

    self._text = text
    self._idx = idx

  #----------------------------------------------------------------------------#
  def on_pop( self, event ):
    self.pop_from.emit(self._idx + 1)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CrumbBar( QtWidgets.QWidget ):
  crumb_popped = QtCore.Signal(int)

  def __init__(self,
    manager ):

    super().__init__()

    self._manager = manager

    self._hlayout = QtWidgets.QHBoxLayout(self)
    self._hlayout.setSpacing(0)
    self._hlayout.setContentsMargins(0,0,0,0)

    self.setLayout(self._hlayout)

    self._hlayout.addStretch()
    self._crumbs = list()

  #-----------------------------------------------------------------------------
  def crumb_push( self, name ):

    idx = len(self._crumbs)

    crumb = Crumb(idx, name)
    crumb.pop_from.connect(self.on_crumb_popped)

    self._hlayout.insertWidget( idx, crumb )
    self._crumbs.append(crumb)


  #-----------------------------------------------------------------------------
  def on_crumb_popped( self, idx ):

    last = len(self._crumbs)-1

    for i in range(last, idx-1, -1):
      crumb = self._crumbs.pop()

      self._hlayout.removeWidget( crumb )
      crumb.setParent( None )

      self.crumb_popped.emit(i)
