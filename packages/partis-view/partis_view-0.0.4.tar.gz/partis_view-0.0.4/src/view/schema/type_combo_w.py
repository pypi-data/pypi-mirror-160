# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

#
from partis.view.edit.var_tree import (
  VariableTree,
  VariableTreeItem )

from partis.view.base import (
  ToolButton,
  ScrollComboBox )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TypeComboWidget ( QtWidgets.QWidget ):

  changed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    label_data,
    init_data = None,
    readonly = None ):
    super().__init__()

    self._label_data = label_data

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.types_combo = ScrollComboBox()
    self.types_combo.readonly = readonly

    for label, data in label_data:
      self.types_combo.addItem( label, userData = data )

    self.types_combo.currentIndexChanged.connect( self.on_changed )

    self.layout.addWidget( self.types_combo )

    if init_data is not None:
      self.set( init_data )

  #-----------------------------------------------------------------------------
  def on_changed( self, index ):
    self.changed.emit( self._label_data[index][1] )

  #-----------------------------------------------------------------------------
  def set( self, data ):
    index = self.types_combo.findData( data )

    if index >= 0:
      self.types_combo.setCurrentIndex( index )
