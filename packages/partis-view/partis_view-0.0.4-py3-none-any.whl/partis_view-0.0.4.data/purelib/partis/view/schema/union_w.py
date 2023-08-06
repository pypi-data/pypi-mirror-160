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
  is_evaluated,
  Loc,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim )

from .tree_edit_w import (
  TreeEditItem,
  TreeEditNode )

prim_names = {
  'bool' : BoolPrim,
  'int' : IntPrim,
  'float' : FloatPrim,
  'string' : StrPrim,
  'list' : SeqPrim,
  'dict' : MapPrim }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionTreeEditNode( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    super().__init__( *args, **kwargs, editable = False )

  #-----------------------------------------------------------------------------
  def build_type( self ):

    self._cur_case = None
    self._state_cases = [ None for i in range(len(self._schema.cases)) ]

    self._cases = list()

    for i, case in enumerate( self._schema.cases ):
      if is_schema_struct( case ):
        name = case.tag
      else:
        schema = case.schema

        for name, cls in prim_names.items():
          if isinstance( schema, cls ):
            break
        else:
          name = case.__name__

      self._cases.append( ( name, i ) )

    if self._expr:
      self._cases.append( ( 'eval', -1 ) )

    self._case_combo = TypeComboWidget(
      label_data = self._cases,
      readonly = self.readonly )


    self._tree.setItemWidget( self._tree_item, self.COL_TYPE, self._case_combo )

    self._case_combo.changed.connect( self.on_set_case )

    # TODO: discover why hiding case_combo does not hide, but hiding types_combo does
    # self._case_combo.setVisible(not self.readonly)
    self._case_combo.types_combo.setVisible(not self.readonly)

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is not None:
      assert is_valued_type( state )

      # set case based on initial state
      for i, case in enumerate(self._schema.cases):

        # if issubclass( state._schema, case.schema ):
        if state._schema is case.schema:
          self._state_cases[i] = state
          self.set_case( case = i )
          break

      else:
        raise ValueError(f"state schema not a case: {state._schema}, {self._schema.cases}")


    elif not is_required( self._schema.default_case ):
      # set case based on schema default case
      self.set_case( case = self._schema.default_case )

    else:
      # set to first case
      self.set_case( case = 0 )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_case( self, case ):

    if case == -1:
      # NOTE: special case to switch to evaluated input since combo box will take
      # the place of the button
      self.on_expr_toggle()
      return

    if self._cur_case == case:
      if 'main' in self._tree_nodes:
        with blocked( self._tree_nodes['main'] ):
          self._tree_nodes['main'].set_state(
            state = self._state_cases[ self._cur_case ] )

      return

    with blocked( self._case_combo ):
      self._case_combo.set( case )

    self._cur_case = case

    # attempt to use a previously set state for the new case

    state = self._state_cases[ self._cur_case ]

    if state is None:
      # if not yet edited, create a new default state
      _schema = self._schema.cases[ self._cur_case ].schema

      state = _schema.decode(
        val = _schema.init_val,
        loc = self._loc )

      assert state is not None

      self._state_cases[ self._cur_case ] = state

    if 'main' in self._tree_nodes:
      child = self._tree_nodes['main']
      child.close()

      self._tree_item.takeChildren()

      self._tree_item.setData( self.COL_KEY, QtCore.Qt.EditRole, self )
      self._tree_item.setData( self.COL_SUBEDIT, QtCore.Qt.EditRole, self )
      self._tree_item.setData( self.COL_TYPE, QtCore.Qt.EditRole, self )
      self._tree_item.setData( self.COL_EDIT, QtCore.Qt.EditRole, self )

      # reset the flags and data in case they have been altered by child
      self._tree_item.setFlags( QtCore.Qt.ItemIsEnabled )

    # create new widgets for the tree and editor for this state
    child = self._tree_node_map( schema = state._schema, state = state )(
      manager = self._manager,
      parent_node = self,
      tree_widget = self._tree_widget,
      tree_item = self._tree_item,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = state._schema,
      # Expressions are handled at the union level, and not at the case level.
      expr_enabled = False,
      state = state,
      readonly = self.readonly )

    # key column should always point to the union
    self._tree_item.setData( self.COL_KEY, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_SUBEDIT, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_TYPE, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_EDIT, QtCore.Qt.EditRole, self )

    child.state_changed.connect( self.on_child_state_changed )
    child.expr_toggled.connect( self.on_child_expr_toggled )

    self._tree_nodes['main'] = child

    # log.debug(f"adding {type(child)} ({type(self)}, {id(self)})")

    super().set_state( state = state )

  #-----------------------------------------------------------------------------
  def on_set_case( self, case ):
    self.set_case( case )
    self.expanded = True

  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):

    self._state_cases[ self._cur_case ] = state
    self.state = state

    # self.state_changed.emit( self._key, state )

  #-----------------------------------------------------------------------------
  def on_child_expr_toggled( self, key, active ):
    self.expr_toggled.emit( self._key, active )

  #-----------------------------------------------------------------------------
  def set_expanded(self, val):
    super().set_expanded( val )

    for k,v in self.nodes:
      v.expanded = val

  #-----------------------------------------------------------------------------
  def display_text(self):
    if 'main' in self._tree_nodes:
      return self._tree_nodes['main'].display_text()

    return ""

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):
    if 'main' in self._tree_nodes:
      return self._tree_nodes['main'].build_editor(parent, full)

    return None

  #-----------------------------------------------------------------------------
  def bg_color( self, col ):
    if 'main' in self._tree_nodes:
      return self._tree_nodes['main'].bg_color(col)

    return None
