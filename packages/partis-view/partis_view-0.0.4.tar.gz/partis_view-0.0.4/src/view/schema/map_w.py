# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict )

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
  TreeEditItem,
  TreeEditNode )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MapTreeEditNode( TreeEditNode ):
  allowed_as_root = True

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    super().__init__( *args, **kwargs, editable = False )

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    if not self.readonly:
      self._add_tree_item = TreeEditItem( self._tree_item )

      self._add_btn = ToolButton(
        self._manager.resource_path('images/icons/add.svg'),
        "Add Struct Item" )

      self._add_btn.clicked.connect( self.on_child_added )
      # self._add_tree_item.clicked.connect( self.on_add_tree_item_clicked )

      self._tree.setItemWidget( self._add_tree_item, self.COL_TYPE, self._add_btn )
      self._add_tree_item.setText( self.COL_INDEX, "z" )


  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    # remove keys not longer in state
    for k in list(self._tree_nodes.keys()):
      if k not in state:
        self.delete_child( k )

    # add keys not currently in item
    for i, (k, v) in enumerate( state.items() ):
      if k not in self._tree_nodes:
        # create new widgets for the tree and editor for this state
        self.create_child(
          key = k,
          index = i,
          state = v )

      else:
        # update state of item
        with blocked( self._tree_nodes[k] ):
          self._tree_nodes[k].set_state( state = v )
          self._tree_nodes[k].index = i

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    if self._schema.min_len:
      removable = len(state) > self._schema.min_len

      for k, v in self._tree_nodes.items():
        v.removable = removable

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def create_child( self,
    state = None,
    key = None,
    index = None ):

    child = super().create_child(
      schema = self._schema.item.schema,
      state = state,
      movable = True,
      removable = True,
      key = key,
      key_edit = True,
      index = index )

    return child

  #-----------------------------------------------------------------------------
  def on_add_tree_item_clicked ( self, col ):
    self.on_child_added()

  #-----------------------------------------------------------------------------
  def on_child_added( self ):

    child = self.create_child(
      index = len(self._state) )

    child.expanded = True

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    state = copy( self.state )

    state[ child._key ] = child.state

    self.state = state

    if self._schema.min_len:
      removable = len(state) > self._schema.min_len

      for k, v in self._tree_nodes.items():
        v.removable = removable

  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):

    _state = copy( self.state )

    _state[key] = state

    self.state = _state

  #-----------------------------------------------------------------------------
  def on_child_moved_down( self, key ):

    child = self._tree_nodes[key]

    index = child._index

    items = list(self.state.items())

    if index < len(items)-1:
      item = items[ index+1 ]
      _child = self._tree_nodes[ item[0] ]

      items[ index+1 ] = items[ index ]
      items[ index ] = item

      child.index = index+1
      _child.index = index

      self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

      state = self._schema.decode( odict(items) )
      self.state = state

  #-----------------------------------------------------------------------------
  def on_child_moved_up( self, key ):

    child = self._tree_nodes[key]

    index = child._index

    items = list(self.state.items())

    if len(items) > 1 and index > 0:
      item = items[ index-1 ]
      _child = self._tree_nodes[ item[0] ]

      items[ index-1 ] = items[ index ]
      items[ index ] = item

      child.index = index-1
      _child.index = index

      self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

      state = self._schema.decode( odict(items) )
      self.state = state

  #-----------------------------------------------------------------------------
  def on_child_removed( self, key ):
    self.delete_child( key )

    state = copy( self.state )
    state.pop( key )
    self.state = state

    if self._schema.min_len:
      removable = len(state) > self._schema.min_len

      for k, v in self._tree_nodes.items():
        v.removable = removable

  #-----------------------------------------------------------------------------
  def on_child_key_changed( self, key, new_key ):
    self._tree_nodes[new_key] = self._tree_nodes.pop(key)

    state = copy(self.state)
    state[new_key] = state.pop(key)
    self.state = state

  #-----------------------------------------------------------------------------
  def on_child_expr_toggled( self, key, active ):

    state = self._tree_nodes[key].state
    index = self._tree_nodes[key]._index

    if hasattr( self._tree_nodes[key], '_bak_state'):
      _state = self._tree_nodes[key]._bak_state
    else:
      _state = None

    if _state is None:
      if active:
        schema = self._schema.item.schema
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
      index = index,
      state = _state )

    child._bak_state = state

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )

  #-----------------------------------------------------------------------------
  def display_text(self):
    if not self._tree_item.isExpanded():
      num = len(self.state)

      if num:
        return f"+ {num} items"

    return ""
