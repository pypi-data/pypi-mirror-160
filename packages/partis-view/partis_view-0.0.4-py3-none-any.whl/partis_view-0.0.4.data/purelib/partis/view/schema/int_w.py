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
  blocked )

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

from .edit_w import (
  Edit,
  RestrictedEdit )

from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntValidator ( QtGui.QIntValidator ):
  #----------------------------------------------------------------------------#
  def __init__ ( self, schema ):
    super().__init__()

    self._schema = schema
    self._default = schema.default_val

    if is_required(self._default) or is_optional(self._default):
      self._default = 0

      if schema.min is not None and self._default < schema.min:
        self._default = schema.min

      elif schema.max is not None and self._default > schema.max:
        self._default = schema.max


    if schema.min is not None:
      self.setBottom( schema.min )

    if schema.max is not None:
      self.setTop( schema.max )

  #----------------------------------------------------------------------------#
  def set_default( self, val ):
    self._default = val

  #-----------------------------------------------------------------------------
  def format( self, val ):
    return f"{val:d}"

  #----------------------------------------------------------------------------#
  def fixup( self, input ):

    valid = self.validate(input, 0)

    if valid == QtGui.QValidator.Acceptable:
      return input
    else:
      # revert to previously valid valid
      return self.format( self._default )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._validator = IntValidator( self._schema )

    self._line = QtWidgets.QLineEdit( self._validator.format( self._validator._default ) )

    self._line.setReadOnly( self.readonly )

    self._line.setValidator( self._validator )

    self._line.textChanged.connect( self.on_changed )
    self._line.editingFinished.connect( self.on_finished_line )

    self._layout.addWidget( self._line )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    self._validator.set_default( state )

    with blocked( self._line ):
      self._line.setText( self._validator.format( state ) )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._line.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_changed( self, text ):
    try:
      val = int(text)
      self._validator.set_default( val )
    except:
      pass

  #-----------------------------------------------------------------------------
  def on_finished_line( self ):

    self._state = self._schema.decode(
      val = int(self._line.text()),
      loc = self._loc )

    with blocked( self._line ):
      self._line.setText( self._validator.format( self._state ) )

    self.state_changed.emit( self._state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntTreeEditNode ( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    if self._schema.restricted is not None:
      editor = RestrictedEdit(
        manager = self._manager,
        schema = self._schema,
        parent = parent,
        loc = self._loc,
        readonly = self.readonly )

    else:
      editor = IntEdit(
        manager = self._manager,
        schema = self._schema,
        parent = parent,
        loc = self._loc,
        readonly = self.readonly )

    return editor

  #----------------------------------------------------------------------------#
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def display_text(self):

    return f"{self.state._encode}"
