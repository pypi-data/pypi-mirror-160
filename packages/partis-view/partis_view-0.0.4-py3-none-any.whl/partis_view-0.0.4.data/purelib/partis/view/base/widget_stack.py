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

from .crumbs import CrumbBar

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WidgetStack( QtWidgets.QWidget ):

  finished = QtCore.Signal(int)

  def __init__(self,
    manager ):

    super().__init__()

    self._manager = manager

    self._stack = QtWidgets.QStackedWidget()
    self._focus_stack = list()

    self._crumbs = CrumbBar(
      self._manager )

    self._crumbs.crumb_popped.connect( self.pop_widget )

    self._crumbs.setVisible( False )

    self._vlayout = QtWidgets.QVBoxLayout(self)
    self._vlayout.setSpacing(0)
    self._vlayout.setContentsMargins(0,0,0,0)

    self.setLayout(self._vlayout)

    self._vlayout.addWidget( self._crumbs )
    self._vlayout.addWidget( self._stack )

    self.setVisible( False )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def push_widget( self, widget, name = None ):

    if name is None:
      if self._stack.count() == 0:
        name = "..."
      else:
        name = str(self._stack.count())

    self.setVisible( True )
    self._crumbs.crumb_push( name )

    if self._stack.count() >= 1:
      self._crumbs.setVisible( True )

    index = self._stack.addWidget( widget )
    self._stack.setCurrentIndex( index )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def pop_widget( self, idx ):

    w = self._stack.currentWidget()

    if hasattr( w, "on_widget_stack_pop" ):
      w.on_widget_stack_pop()

    self._stack.removeWidget( w )
    self._stack.setCurrentIndex( self._stack.count() - 1 )

    if self._stack.count() <= 1:
      self._crumbs.setVisible( False )

      if self._stack.count() == 0:
        # make invisible when no more widgets on stack
        self.setVisible( False )

    if self._stack.count() > 0:
      # set focus to last child widget of revealed stack widget to have had focus
      w = self._stack.currentWidget()
      w_focus = w.focusWidget()

      if w_focus is not None:
        w_focus.setFocus()

  #-----------------------------------------------------------------------------
  def keyPressEvent( self, event ):

    # override tabs to use space delimeter
    if event.key() == QtCore.Qt.Key_Escape and self._stack.count() > 1:
      # only apply ESC key if button is visible

      self.pop_widget(self._stack.count()-1)
      event.accept()
      return

    return super().keyPressEvent( event )
