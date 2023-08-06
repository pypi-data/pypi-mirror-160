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

from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OptionalTreeEditNode( TreeEditNode ):
  option_added = QtCore.Signal( str )

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    super().__init__( *args, **kwargs, editable = False )

  #-----------------------------------------------------------------------------
  def build_type( self ):

    if not self.readonly:

      self._add_btn = ToolButton(
        self._manager.resource_path('images/icons/add.svg'),
        "Add Option" )

      self._add_btn.clicked.connect( self.on_option_added )

      self._tree.setItemWidget( self._tree_item, self.COL_TYPE, self._add_btn )

  #----------------------------------------------------------------------------#
  def on_option_added( self ):
    self.option_added.emit( self._key )

  #-----------------------------------------------------------------------------
  def display_text(self):
    if self.readonly:
      return "None"

    return ""
