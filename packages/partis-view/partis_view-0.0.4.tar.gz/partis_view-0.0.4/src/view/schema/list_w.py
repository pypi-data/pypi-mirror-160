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
  TreeEditItem,
  TreeEditNode )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ListTreeEditNode( TreeEditNode ):
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
        "Add List Item" )

      self._add_btn.clicked.connect( self.on_child_added )

      self._tree.setItemWidget( self._add_tree_item, self.COL_TYPE, self._add_btn )
      self._add_tree_item.setText( self.COL_INDEX, "z" )


  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    # remove keys not longer in state
    d = [ v for k, v in self._tree_nodes.items() if int(k) >= len(state) ]

    for child in d:
      self.delete_child( child._key )

    # add keys not currently in item
    for i, v in enumerate( state ):
      k = str(i)

      if k not in self._tree_nodes:
        self.create_child(
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
    index = None ):

    if index is None:
      index = len(self._tree_nodes)

    key = str(index)

    if key in self._tree_nodes:
      # move all other children up in list
      for i in range( len(self._tree_nodes)-1, index-1, -1 ):
        old_key = str(i)
        new_key = str(i+1)

        child = self._tree_nodes[old_key]
        child.key = new_key
        child.index = i+1
        self._tree_nodes[new_key] = child

      self._tree_nodes.pop(key)

    child = super().create_child(
      schema = self._schema.item.schema,
      state = state,
      movable = True,
      removable = True,
      key = key,
      key_edit = False,
      index = index )

    return child

  #-----------------------------------------------------------------------------
  def delete_child( self, key ):

    index = self._tree_nodes[key]._index

    super().delete_child( key = key )

    # move all other children down in list

    old_key = None

    for i in range( index, len(self._tree_nodes) ):
      old_key = str(i+1)
      new_key = str(i)

      child = self._tree_nodes[old_key]
      child.key = new_key
      child.index = i
      self._tree_nodes[new_key] = child

    if old_key is not None:
      self._tree_nodes.pop(old_key)

  #-----------------------------------------------------------------------------
  def on_child_added( self ):

    child = self.create_child(
      index = len(self._state) )

    child.expanded = True

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    state = copy( self.state )
    state.append( child.state )
    self.state = state

  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):

    i = int(key)
    _state = copy(self.state)
    _state[i] = state
    self.state = _state

  #-----------------------------------------------------------------------------
  def on_child_moved_up( self, key ):

    state = copy(self._state)

    child = self._tree_nodes[key]

    index = child._index
    _index = index - 1

    if len(state) > 1 and index > 0:
      item = state[ _index ]
      _child = self._tree_nodes[ str(_index) ]

      state[ _index ] = state[ index ]
      state[ index ] = item

      child.key = str(_index)
      child.index = _index
      self._tree_nodes[ str(_index) ] = child

      _child.key = key
      _child.index = index
      self._tree_nodes[key] = _child

      self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

      self.state = state

  #-----------------------------------------------------------------------------
  def on_child_moved_down( self, key ):

    state = copy(self.state)

    child = self._tree_nodes[key]

    index = child._index
    _index = index + 1

    if index < len(state)-1:
      item = state[ _index ]
      _child = self._tree_nodes[ str(_index) ]

      state[ _index ] = state[ index ]
      state[ index ] = item

      child.key = str(_index)
      child.index = _index
      self._tree_nodes[ str(_index) ] = child

      _child.key = key
      _child.index = index
      self._tree_nodes[key] = _child

      self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

      self.state = state

  #-----------------------------------------------------------------------------
  def on_child_removed( self, key ):

    index = self._tree_nodes[key]._index

    self.delete_child( key )

    state = copy( self.state )
    val = state.pop( index )
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
      index = index,
      state = _state )

    child._bak_state = state

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )

  #-----------------------------------------------------------------------------
  def on_child_key_changed( self, key, new_key ):
    pass

  #-----------------------------------------------------------------------------
  def display_text(self):
    if not self._tree_item.isExpanded():
      num = len(self.state)

      if num:
        return f"+ {num} items"

    return ""
