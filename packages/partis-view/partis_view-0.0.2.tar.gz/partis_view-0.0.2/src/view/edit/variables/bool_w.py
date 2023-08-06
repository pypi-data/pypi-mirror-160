# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import ClickLabel, blocked
from .base import VariableWidget
from ..var_tree import VariableTreeItem

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolWidget ( VariableWidget ):

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

    if self._tree_parent is not None:
      self.checkbox = QtWidgets.QCheckBox( )

      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 1, self.checkbox )
      self._tree_item._tree.setItemWidget( self._tree_item, 4, self )

      self._tree_item.clicked.connect( self.on_tree_item_clicked )

      if type.info is not None:
        tooltip = "<FONT>" + type.info + "</FONT>"
        self._tree_item.setToolTip( 0, tooltip )
        self._tree_item.setToolTip( 2, tooltip )

    else:
      self.checkbox = QtWidgets.QCheckBox( type.label )

      if type.info is not None:
        tooltip = "<FONT>" + type.info + "</FONT>"
        self.checkbox.setToolTip( tooltip )

      self.hlayout = QtWidgets.QHBoxLayout()
      self.setLayout(self.hlayout)
      self.hlayout.addWidget( self.checkbox )
      self.hlayout.addStretch()

    self.checkbox.stateChanged.connect( self.on_change )


  #-----------------------------------------------------------------------------
  def on_tree_item_clicked ( self, col ):
    if not self._tree_item.isDisabled() and col == 2:
      # don't block signals, since this simulates clicking the checkbox
      self.checkbox.setChecked( not self.checkbox.isChecked() )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )
      self.checkbox.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):
    with blocked( self.checkbox ):
      self.checkbox.setChecked( value )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    return self._type.cast( self.checkbox.isChecked() )

  #----------------------------------------------------------------------------#
  def on_change( self, _ ):
    self.changed.emit( self.get_value() )
