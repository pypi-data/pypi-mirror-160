# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy
from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  ModelHint,
  hint_level_num,
  hint_level_name,
  HINT_LEVELS )

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked )

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

from partis.schema import (
  is_required,
  is_optional,
  is_sequence,
  is_schema_struct,
  is_valued_type,
  Loc )

from partis.view.dialog import (
  LogWidget )

from .str_w import (
  StrMultilineEdit )

from partis.view.schema import (
  TreeEditNode,
  TreeEditWidget,
  StructTreeEditNode,
  ListTreeEditNode,
  Edit )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def rgb( r, g, b ):
  return r, g, b

ALPHA = 32

LEVEL_COLORS = {
  'NOTSET' : QtGui.QColor( *rgb(233, 142, 235), ALPHA ),
  'TRACE' : QtGui.QColor( *rgb(197, 74, 255), ALPHA ),
  'DEBUG' : QtGui.QColor( *rgb(154, 74, 255), ALPHA ),
  'DEBUG' : QtGui.QColor( *rgb(71, 144, 254), ALPHA ),
  'INFO' : QtGui.QColor( *rgb(103, 255, 150), ALPHA ),
  'WARNING' : QtGui.QColor( *rgb(250, 176, 66), ALPHA ),
  'ERROR' : QtGui.QColor( *rgb(252, 93, 71), ALPHA ),
  'CRITICAL' : QtGui.QColor( *rgb(255, 95, 73), ALPHA ) }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def max_level_name( state ):

  num = 0
  msg = ""

  if is_sequence( state ):
    for v in state:
      _num = hint_level_num(v['level'])

      num = max( num, _num )

      if _num == num:
        msg = v['msg']
  else:
    return v['level'], v['msg']

  return hint_level_name(num), msg

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def state_to_hint( state ):
  return ModelHint(
    msg = state['msg'],
    loc = state['loc'],
    level = state['level'],
    hints = [ state_to_hint(v) for v in state['hints'] ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LevelCombo( QtWidgets.QWidget ):
  level_changed = QtCore.Signal( str )

  def __init__(self):
    super().__init__()

    self._level_layout = QtWidgets.QHBoxLayout(self)
    self.setLayout(self._level_layout)

    self._level_layout.addWidget(QtWidgets.QLabel("Filter by level "), 0)

    self.log_level_combo = QtWidgets.QComboBox()

    for label, num, doc in HINT_LEVELS:
      self.log_level_combo.addItem( label, userData = label )

    self.log_level_combo.setCurrentIndex(
      self.log_level_combo.findData( 'NOTSET' ) )

    self.log_level_combo.currentIndexChanged.connect( self.on_change_level )

    self._level_layout.addWidget(
      self.log_level_combo, 1 )

  #-----------------------------------------------------------------------------
  def on_change_level( self ):
    self.level_changed.emit( self.log_level_combo.currentData() )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._level_combo = LevelCombo()
    self._level_combo.level_changed.connect( self.on_change_level )

    self._layout.addWidget(
      self._level_combo )

    self._tree_editor = TreeEditWidget(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._get_eval_names,
      schema = self._schema,
      readonly = self.readonly )

    self._layout.addWidget( self._tree_editor )

  #-----------------------------------------------------------------------------
  def on_change_level( self, level ):

    with blocked( self._tree_editor ):
      hints = list()

      for hint in self.state.hints:
        hints.extend( ModelHint.filter( hint, level = level ) )

      state = copy(self.state)
      state.hints = hints

      self._tree_editor.set_state( state )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._tree_editor ):
      self._tree_editor.set_state( state )

    self._level_combo.setVisible(len(state.hints) > 1)

    super().set_state( state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintListEdit( Edit ):
  """Used for special rendering of logs in 'readonly' mode
  """
  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._level_combo = LevelCombo()
    self._level_combo.level_changed.connect( self.on_change_level )

    self._layout.addWidget(
      self._level_combo )

    self._tree_editor = TreeEditWidget(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._get_eval_names,
      schema = self._schema,
      readonly = self.readonly )

    self._layout.addWidget( self._tree_editor )

  #-----------------------------------------------------------------------------
  def on_change_level( self, level ):

    with blocked( self._tree_editor ):
      hints = list()

      for hint in self.state:
        hints.extend( ModelHint.filter( hint, level = level ) )

      self._tree_editor.set_state( self._schema.decode(
        val = hints,
        loc = self._loc ) )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._tree_editor ):
      self._tree_editor.set_state( state )

    super().set_state( state )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintListNode( ListTreeEditNode ):

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    readonly = None,
    subedit = None,
    **kwargs ):

    super().__init__(
      **kwargs,
      readonly = readonly,
      # allow a sub-editor so that in read-only the logs are displayed with
      # better formatting using the HintListEdit
      subedit = bool(readonly) )


  #-----------------------------------------------------------------------------
  # def set_state( self, state ):
  #
  #   if state is None:
  #     state = self._schema.decode(
  #       val = self._schema.init_val,
  #       loc = self._loc )
  #
  #   if self.readonly:
  #     # render as a normal node instead of all logs in the main tree
  #     TreeEditNode.set_state( self, state )
  #
  #   else:
  #
  #     super().set_state( state )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):
    # will only be built as sub-editor when readonly
    editor = HintListEdit(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._tree_widget._get_eval_names,
      schema = self._schema if full else self._schema.msg,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly )

    return editor

  #-----------------------------------------------------------------------------
  def display_text(self):
    if not self._tree_item.isExpanded():
      num = len(self.state)

      if num:
        level, msg = max_level_name( self.state )
        return f"+ {num} items, {level} \"{msg}\""

    return ""

  #-----------------------------------------------------------------------------
  def bg_color( self, col ):
    if not self._tree_item.isExpanded() and len(self.state) > 0:
      level, msg = max_level_name( self.state )

      if level in LEVEL_COLORS:
        return LEVEL_COLORS[level]

    return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintNode( StructTreeEditNode ):
  allowed_as_root = False

  #-----------------------------------------------------------------------------
  def __init__( self, *,
    parent_node,
    readonly = None,
    subedit = None,
    editable = None,
    **kwargs ):

    TreeEditNode.__init__(
      self,
      **kwargs,
      parent_node = parent_node,
      readonly = readonly,
      # allow a sub-editor so that in read-only the logs are displayed with
      # better formatting using the HintListEdit
      subedit = bool(readonly) and parent_node is not None,
      editable = False )

  #-----------------------------------------------------------------------------
  def create_child( self,
    key,
    state = None ):

    if self.readonly:
      # only add if not readonly
      if key == "level":
        return
      elif key == "hints" and ( not state or len(state) == 0 ):
        # only add if 1 or more sub-hints
        return

    super().create_child( key, state )

  #-----------------------------------------------------------------------------
  def display_text(self):
    if not self._tree_item.isExpanded():
      num = len(self.state.hints)

      if num:
        return f"+ {num} items, {self.state.level} \"{self.state.msg}\""

      return f"{self.state.level} \"{self.state.msg}\""

    if self.readonly:
      return f"{self.state.level}"

    return ""

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):
    from .tree_edit_w import TreeEdit

    editor = HintEdit(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._tree_widget._get_eval_names,
      schema = self._schema if full else self._schema.msg,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly )

    return editor

  #-----------------------------------------------------------------------------
  def set_state_editor( self, state, full ):
    if full:
      self._state = state
    else:
      self._state = copy( self._state )
      self._state.msg = state

    self.state_changed.emit( self._key, self._state )

  #-----------------------------------------------------------------------------
  def get_state_editor( self, full ):
    if full:
      return self._state
    else:
      return self._state.msg

  #-----------------------------------------------------------------------------
  def bg_color( self, col ):
    level = self.state.level

    if level in LEVEL_COLORS:
      return LEVEL_COLORS[level]

    return None
