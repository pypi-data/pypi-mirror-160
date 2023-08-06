# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy
from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.view.base import (
  blocked,
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  EditLabel )

from partis.view.edit.var_tree import (
  VariableTree,
  VariableTreeItem )

from .type_combo_w import TypeComboWidget

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

from partis.schema import (
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_required,
  is_optional,
  is_schema_struct,
  is_valued_type,
  NotEvaluated,
  Loc )

from partis.utils import (
  odict )

from .name_w import (
  RenameDialog )

from .edit_w import Edit

from .tree_edit_node import (
  TreeEditItem,
  TreeEditNode )

from .tree_edit_deligate import (
  EditDeligate )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeEditWidget( QtWidgets.QWidget ):
  state_changed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema,
    tree_node_map = None,
    detail_widget_map = None,
    get_eval_names = None,
    state = None,
    readonly = None ):

    super().__init__()

    if tree_node_map is None:
      # default node mapping
      from . import TreeEditNodeMap
      tree_node_map = TreeEditNodeMap()

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.setFocusPolicy( QtCore.Qt.StrongFocus )

    self._manager = manager
    self._widget_stack = widget_stack
    # schema.schema ensures its not a proxy
    self._schema = schema.schema
    self._tree_node_map = tree_node_map
    self._detail_widget_map = detail_widget_map
    self._get_eval_names = get_eval_names
    self._state = None
    self._readonly = readonly

    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.config_tree = VariableTree(
      manager = manager,
      ncols = TreeEditNode.NUM_COLS )

    self._edit_delegate = EditDeligate(
      tree = self.config_tree )

    # self.config_tree.setItemDelegateForColumn(
    #   TreeEditNode.COL_EDIT,
    #   self._edit_delegate )

    self.config_tree.setItemDelegate(
      self._edit_delegate )

    # self.config_tree.setEditTriggers(
    #   QtWidgets.QAbstractItemView.DoubleClicked
    #   | QtWidgets.QAbstractItemView.SelectedClicked )

    self.config_tree.setExpandsOnDoubleClick( False )

    self.config_tree_area = QtWidgets.QScrollArea()
    self.config_tree_area.setWidgetResizable( True )
    policy = QtWidgets.QSizePolicy.Expanding
    self.config_tree_area.setSizePolicy( QtWidgets.QSizePolicy(policy, policy) )

    inner = QtWidgets.QFrame(self.config_tree_area)
    inner.setLayout(QtWidgets.QVBoxLayout())
    inner.layout().setSpacing(0)
    inner.layout().setContentsMargins(0,0,0,0)

    self.config_tree_area.setWidget( inner )

    inner.layout().addWidget( self.config_tree )

    self.layout.addWidget( self.config_tree_area )

    node_cls = tree_node_map( schema = self._schema, state = state )

    if node_cls.allowed_as_root:
      tree_item = self.config_tree.invisibleRootItem()
      tree_item._tree = self.config_tree

    else:
      tree_item = TreeEditItem(
        parent = self.config_tree )

    self._tree_root_node = node_cls(
      manager = self._manager,
      parent_node = None,
      tree_widget = self,
      tree_item = tree_item,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = self._schema,
      state = state,
      readonly = self._readonly )

    # expand first level of nodes
    self.root_node.expanded = True

    # for k, v in self.root_node.nodes.items():
    #   v.expanded = True

    self.root_node.state_changed.connect( self.on_tree_node_changed )

    self.config_tree.hideColumn( self.root_node.COL_INDEX )
    self.config_tree.updateGeometry()

    # self.config_tree.installEventFilter( self )

  #-----------------------------------------------------------------------------
  @property
  def root_node(self):
    return self._tree_root_node

  #-----------------------------------------------------------------------------
  def close_editors( self ):
    self._edit_delegate.close_editors()

  #-----------------------------------------------------------------------------
  def setFocus( self ):
    self.config_tree.setFocus()

  #-----------------------------------------------------------------------------
  def mousePressEvent( self, event ):
    if event.button() == QtCore.Qt.LeftButton:
      self.close_editors()

  #-----------------------------------------------------------------------------
  def on_expanded( self, index ):
    pass

  #-----------------------------------------------------------------------------
  def on_collapsed( self, index ):
    # TODO: this could be more elegant, and would be better if it only closed
    # editor if the editor is on the branch that was collapsed.
    self.close_editors()

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  @state.setter
  def state( self, state ):
    self._state = state
    self.state_changed.emit( state )

  #-----------------------------------------------------------------------------
  def on_tree_node_changed( self, key, state ):

    self.state = state

    # self.config_tree.updateGeometries()

  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    with blocked( self.root_node ):
      self.root_node.set_state( state )

    self.state = state

  #-----------------------------------------------------------------------------
  def get_eval_names( self, context = None ):
    if self._get_eval_names:
      return self._get_eval_names( context = context )

    return dict()

  #-----------------------------------------------------------------------------
  async def test_schema_tree( self ):
    # TODO: add tests, traversing the tree and doing 'something' that might cause an error
    # assert(False)
    pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._tree_editor = TreeEditWidget(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._get_eval_names,
      schema = self._schema,
      readonly = self.readonly )

    self._layout.addWidget( self._tree_editor )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._tree_editor ):
      self._tree_editor.set_state( state )

    super().set_state( state )
