# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import blocked
from .base import VariableWidget
from ..var_tree import VariableTreeItem

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ArrayWidget ( VariableWidget ):

  changed = QtCore.Signal(object)

  #----------------------------------------------------------------------------#
  def __init__ ( self, manager, type, config, tree_parent = None ):
    super().__init__()

    self._manager = manager
    self._type = type
    self._config = config
    self._tree_parent = tree_parent
    self._tree_item = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.widgets = []

    if self._tree_parent is not None:
      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 4, self )

      if type.info is not None:
        tooltip = "<FONT>" + type.info + "</FONT>"
        self._tree_item.setToolTip( 0, tooltip )
        self._tree_item.setToolTip( 1, tooltip )
        self._tree_item.setToolTip( 2, tooltip )

    else:
      self.hlayout = QtWidgets.QHBoxLayout()
      self.setLayout(self.hlayout)

      self.label = QtWidgets.QLabel( type.label )
      self.hlayout.addWidget( self.label )

    from . import var_widgets

    for i, T in enumerate( type._tuple_types ):
      widget = var_widgets[ T.__class__ ](
        manager = manager,
        type = T,
        config = config,
        tree_parent = self._tree_item )

      self.widgets.append( widget )

      if self._tree_item is None:
        self.hlayout.addWidget( widget )

    if self._tree_item is None:
      self.hlayout.addStretch()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )

      for var in self.widgets:
        var.set_enabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):
    for w, v in zip( self.widgets, value ):
      w.set_value( v )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    value = tuple([ w.get_value() for w in self.widgets ])

    return value

  #----------------------------------------------------------------------------#
  def on_change( self ):
    self.changed.emit( self.get_value() )
