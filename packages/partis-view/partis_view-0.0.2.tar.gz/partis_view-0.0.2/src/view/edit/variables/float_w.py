# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from .base import VariableWidget
from ..var_tree import VariableTreeItem

from partis.view.base import blocked

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DoubleValidator ( QtGui.QDoubleValidator ):

  #----------------------------------------------------------------------------#
  def __init__ ( self, type ):
    super().__init__()

    self._type = type

    if type._min is not None:
      self.setBottom( type._min )

    if type._max is not None:
      self.setTop( type._max )

  #----------------------------------------------------------------------------#
  def set_default( self, value ):
    self._default = value

  #----------------------------------------------------------------------------#
  def fixup( self, input ):

    valid = self.validate(input, 0)

    if valid == QtGui.QValidator.Acceptable:
      return input
    else:
      return "{:.3e}".format( self._default )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FloatWidget ( VariableWidget ):

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


    self.line = QtWidgets.QLineEdit( str(self._type._min) if type._min is not None else "0" )

    self.line.editingFinished.connect( self.on_change )

    self.validator = DoubleValidator( self._type )

    self.line.setValidator( self.validator )

    if self._tree_parent is not None:
      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 2, self.line )
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

      if type.info is not None:
        tooltip = "<FONT>" + type.info + "</FONT>"
        self.line.setToolTip( tooltip )
        self.label.setToolTip( tooltip )

      self.hlayout.addWidget( self.label )
      self.hlayout.addWidget( self.line )
      self.hlayout.addStretch()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )
      self.line.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):

    value = self._type.cast( value )
    self.validator.set_default( value )

    with blocked( self.line ):
      self.line.setText( "{:g}".format(value) )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    return self._type.cast( self.line.text() )

  #----------------------------------------------------------------------------#
  def on_change( self ):
    self.changed.emit( self.get_value() )
