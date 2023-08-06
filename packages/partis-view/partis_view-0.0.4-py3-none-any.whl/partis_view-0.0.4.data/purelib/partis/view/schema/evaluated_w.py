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

from partis.view.edit import (
  VariableTreeItem,
  CodeEdit )

from partis.view.highlight import (
  PygmentsHighlighter )

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
  Edit )

from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._support_combo = ScrollComboBox()
    self._support_combo.readonly = self.readonly
    # self._support_combo.setVisible(not self.readonly)

    for k, v in self._schema.evaluated.supported.items():
      if v.lexer is not None:
        self._support_combo.addItem( v.name, userData = v )

    self._support_combo.currentIndexChanged.connect( self.on_support_changed )

    self._multiline = CodeEdit(
      manager = self._manager,
      expanding = False )

    self._multiline.setReadOnly( self.readonly )

    self._multiline.embed_func = True

    self._multiline.textChanged.connect( self.on_finished_multiline )

    self._layout.addWidget( self._support_combo )
    self._layout.addWidget( self._multiline )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._multiline, self._support_combo ):
      res = self._schema.evaluated.check( state._encode )

      if res is not None:
        support, src = res
        self._multiline.setPlainText( src )
        self._multiline.set_lang( support.lexer )

        index = self._support_combo.findData( support )
        self._support_combo.setCurrentIndex( index )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._support_combo.setEnabled( enabled )
    self._multiline.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_support_changed( self, index ):
    support = self._support_combo.currentData()
    self._multiline.set_lang( support.lexer )
    self.on_finished_multiline()

  #-----------------------------------------------------------------------------
  def on_finished_multiline( self ):
    src = self._multiline.toPlainText()

    src = self._schema.evaluated.escaped(
      support = self._support_combo.currentData(),
      src = src )

    self._state = self._schema.decode(
      val = src,
      loc = self._loc )

    self.state_changed.emit( self._state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedTreeEditNode ( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    expr_active = True,
    subedit = True,
    **kwargs ):

    super().__init__(
      expr_active = True,
      subedit = True,
      **kwargs )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    editor = EvaluatedEdit(
      manager = self._manager,
      schema = self._schema,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly )

    editor._multiline.set_external_names(
      names = self._tree_widget.get_eval_names(
        context = self._schema.evaluated.context ) )

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

    return f"\"{self.state._encode}\""
