# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

from .base import VariableWidget

from partis.view.base import blocked

from ..var_tree import VariableTreeItem

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FilepathWidget( VariableWidget ):

  changed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self, manager, type, config, tree_parent = None ):
    super( FilepathWidget, self ).__init__()

    self._manager = manager
    self._type = type
    self._config = config
    self._tree_parent = tree_parent
    self._tree_item = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self._directory = isinstance( type, DirectoryType )
    self._save = isinstance( type, WriteFileType )


    self.select_button = QtWidgets.QPushButton("Select")
    self.filepath_text = QtWidgets.QLineEdit()

    self.select_button.clicked.connect( self.select_file )

    self.filepath_text.editingFinished.connect( self.on_change )

    if self._tree_parent is not None:
      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 1, self.select_button )
      self._tree_item._tree.setItemWidget( self._tree_item, 2, self.filepath_text )
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
        self.select_button.setToolTip( tooltip )
        self.filepath_text.setToolTip( tooltip )
        self.label.setToolTip( tooltip )

      self.hlayout.addWidget( self.label )
      self.hlayout.addWidget( self.select_button )
      self.hlayout.addWidget( self.filepath_text )
      self.hlayout.addStretch()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )
      self.select_button.setEnabled( enabled )
      self.filepath_text.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #-----------------------------------------------------------------------------
  def select_file( self ):
    path = self.filepath_text.text()
    new_path = None

    if self._directory:
      if path != "":
        new_path = QtWidgets.QFileDialog.getExistingDirectory(
          parent = self,
          dir = path )
      else:
        new_path = QtWidgets.QFileDialog.getExistingDirectory(
          parent = self )
    elif self._save:
      if path != "":
        new_path = QtWidgets.QFileDialog.getSaveFileName(
          parent = self,
          dir = path )[0]
      else:
        new_path = QtWidgets.QFileDialog.getSaveFileName(
          parent = self )[0]
    else:
      if path != "":
        new_path = QtWidgets.QFileDialog.getOpenFileName(
          parent = self,
          dir = path )[0]
      else:
        new_path = QtWidgets.QFileDialog.getOpenFileName(
          parent = self )[0]

    if new_path != "":
      self.filepath_text.setText( new_path )

      self.on_change()

  #----------------------------------------------------------------------------#
  def set_value ( self, value ):
    with blocked( self.filepath_text ):
      self.filepath_text.setText( value )

  #----------------------------------------------------------------------------#
  def get_value ( self ):
    return self._type.cast( self.filepath_text.text() )

  #----------------------------------------------------------------------------#
  def on_change( self ):
    self.changed.emit( self.get_value() )
