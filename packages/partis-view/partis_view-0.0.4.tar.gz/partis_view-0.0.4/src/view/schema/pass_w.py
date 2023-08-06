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
class PassTreeEditNode ( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._line = QtWidgets.QLineEdit()

    self._line.editingFinished.connect( self.on_change )


  #----------------------------------------------------------------------------#
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )


    with blocked( self._line ):
      self._line.setText( str(state) )

    super().set_state( state )

  #----------------------------------------------------------------------------#
  def on_change( self ):
    self._state = self._line.text()

    self.state_changed.emit( self._key, self.state )
