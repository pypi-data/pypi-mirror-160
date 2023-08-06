# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from .base import VariableWidget
from ..var_tree import VariableTreeItem

from partis.view.base import blocked

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SelectionWidget ( VariableWidget ):

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


    self.combobox = QtWidgets.QComboBox()

    for label, opt in zip( type.labels, type.opts ):
      self.combobox.addItem( str(label), userData = opt )

    if self._tree_parent is not None:

      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 2, self.combobox )
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
        self.combobox.setToolTip( tooltip )
        self.label.setToolTip( tooltip )

      self.hlayout.addWidget( self.label )
      self.hlayout.addWidget( self.combobox )
      self.hlayout.addStretch()


    self.combobox.currentIndexChanged.connect( self.on_change )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )
      self.combobox.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):

    with blocked( self.combobox ):
      index = self.combobox.findData( self._type._opt_type.cast( value ) )
      self.combobox.setCurrentIndex( index )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    return self.combobox.currentData()

  #----------------------------------------------------------------------------#
  def on_change( self, _ ):
    self.changed.emit( self.get_value() )
