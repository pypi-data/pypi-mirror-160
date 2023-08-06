# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked,
  ScrollComboBox )

from partis.view.edit.var_tree import VariableTreeItem

from .type_combo_w import TypeComboWidget

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

from partis.schema import (
  is_required,
  is_optional,
  is_schema_struct,
  is_valued_type,
  Loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditBase( QtWidgets.QWidget ):
  state_changed = QtCore.Signal( object )
  clicked = QtCore.Signal( )

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    parent = None,
    state = None,
    readonly = None ):

    super().__init__( parent )

    if readonly is None:
      readonly = False

    self._manager = manager
    self._state = None
    self._readonly = bool(readonly)

    self._layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self._layout)

    self._layout.setContentsMargins(0,0,0,0)
    self._layout.setSpacing(0)

    self.build()
    self.set_state( state )

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #-----------------------------------------------------------------------------
  @property
  def readonly( self ):
    return self._readonly

  #-----------------------------------------------------------------------------
  def build( self ):
    pass

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    self._state = state

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

  #-----------------------------------------------------------------------------
  def mousePressEvent( self, event ):
    self.clicked.emit()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Edit( EditBase ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    schema,
    widget_stack = None,
    tree_node_map = None,
    get_eval_names = None,
    parent = None,
    state = None,
    readonly = None,
    loc = None ):

    if loc is None:
      loc = Loc(
        filename = __name__ )

    self._widget_stack = widget_stack
    self._tree_node_map = tree_node_map
    self._get_eval_names = get_eval_names
    self._schema = schema
    self._loc = loc

    super().__init__(
      manager = manager,
      parent = parent,
      state = state,
      readonly = readonly )

  #-----------------------------------------------------------------------------
  def get_eval_names( self, context = None ):
    if self._get_eval_names:
      return self._get_eval_names( context = context )

    return dict()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RestrictedEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._combo = ScrollComboBox()
    self._combo.readonly = self.readonly

    for opt in self._schema.restricted:
      self._combo.addItem( str(opt),
        userData = str(opt) )

    self._combo.currentIndexChanged.connect( self.on_changed_combo )

    self._layout.addWidget( self._combo )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._combo ):
      index = self._combo.findData( state )
      self._combo.setCurrentIndex( index )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._combo.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_changed_combo( self, index ):

    self._state = self._schema.decode(
      val = self._combo.currentData(),
      loc = self._loc )

    self.state_changed.emit( self._state )
