# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy
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
  Loc )

from .tree_edit_w import (
  TreeEditNode,
  TreeEditItem )

from .optional_w import OptionalTreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OptionalChild( ToolButton ):

  child_added = QtCore.Signal(str)

  #-----------------------------------------------------------------------------
  def __init__( self, key ):
    super().__init__(
      self._manager.resource_path('images/icons/add.svg'),
      "Add" )

    self.clicked.connect( self.on_child_added )
    self._key = key

  #-----------------------------------------------------------------------------
  def on_child_added( self ):
    self.child_added.emit( self._key )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructTreeEditNode( TreeEditNode ):
  allowed_as_root = True

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    super().__init__( *args, **kwargs, editable = False )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    for k, v in self._schema.struct.items():

      if state[k] is None:
        if k in self._tree_nodes:
          if not isinstance( self._tree_nodes[k], OptionalTreeEditNode ):
            _state = self._tree_nodes[k].state
            self.delete_child( k )
            self.create_child_option( k, state = _state )

        else:
          self.create_child_option( k )

      elif k not in self._tree_nodes:
        self.create_child( k, state = state[k] )

      elif (
        not isinstance(
          self._tree_nodes[k],
          self._tree_node_map(
            schema = self._schema.struct[k].schema,
            state = state[k] ) )
        or isinstance( self._tree_nodes[k], OptionalTreeEditNode ) ):

        self.delete_child( k )
        self.create_child( k, state = state[k] )

      else:
        child = self._tree_nodes[k]

        with blocked( child ):
          child.set_state( state = state[k] )

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def create_child( self,
    key,
    state = None ):

    if key in self._tree_nodes:
      raise ValueError(f"child key already present: {key}")

    schema = self._schema.struct[key].schema


    index = list(self._schema.struct.keys()).index( key )

    child = self._tree_node_map( schema = schema, state = state )(
      manager = self._manager,
      parent_node = self,
      tree_widget = self._tree_widget,
      tree_item = TreeEditItem(
        parent = self._tree_item ),
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = schema,
      state = state,
      readonly = self.readonly,
      movable = False,
      removable = is_optional( schema.default_val ),
      key = key,
      key_edit = False,
      index = index )

    child._tree_item.node = child

    child.state_changed.connect( self.on_child_state_changed )
    child.removed.connect( self.on_child_removed )
    child.expr_toggled.connect( self.on_child_expr_toggled )

    self._tree_nodes[key] = child

    return child

  #-----------------------------------------------------------------------------
  def create_child_option( self,
    key,
    state = None ):

    if key in self._tree_nodes:
      raise ValueError(f"child key already present: {key}")

    schema = self._schema.struct[key].schema
    index = list(self._schema.struct.keys()).index( key )

    child = OptionalTreeEditNode(
      manager = self._manager,
      parent_node = self,
      tree_widget = self._tree_widget,
      tree_item = TreeEditItem(
        parent = self._tree_item ),
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = schema,
      state = state,
      readonly = self.readonly,
      movable = False,
      removable = False,
      key = key,
      key_edit = False,
      index = index )

    child._tree_item.node = child
    child.option_added.connect( self.on_child_option_added )

    self._tree_nodes[key] = child

  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):

    self._state = copy( self._state )
    self._state[key] = state

    self.state_changed.emit( self._key, self._state )

  #-----------------------------------------------------------------------------
  def on_child_removed( self, key ):
    state = self._tree_nodes[key].state

    self.delete_child( key )
    self.create_child_option(
      key = key,
      state = state )

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, None )

  #-----------------------------------------------------------------------------
  def on_child_option_added( self, key ):

    state = None

    if self._state is not None and self._state[key] is not None:
      state = self._state[key]

    elif self._tree_nodes[key].state is not None:
      state = self._tree_nodes[key].state

    self.delete_child( key )

    child = self.create_child(
      key = key,
      state = state )

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )

  #-----------------------------------------------------------------------------
  def on_child_expr_toggled( self, key, active ):

    state = self._tree_nodes[key].state

    if hasattr( self._tree_nodes[key], '_bak_state'):
      _state = self._tree_nodes[key]._bak_state
    else:
      _state = None

    if _state is None:
      if active:
        schema = self._schema.struct[key].schema
        evaluated = schema.evaluated
        support = next(iter(evaluated.supported.values()))

        _state = schema.decode(
          val = evaluated.escaped( support, str(state._encode) ),
          loc = self._loc )

      else:
        _state = None

    self.delete_child( key )

    child = self.create_child(
      key = key,
      state = _state )

    child._bak_state = state

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )
