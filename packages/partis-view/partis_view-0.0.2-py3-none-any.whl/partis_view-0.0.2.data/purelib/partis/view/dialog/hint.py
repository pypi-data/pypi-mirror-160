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
  hint_level_num )

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
class HintDeligate( QtWidgets.QStyledItemDelegate ):

  def __init__( self, tree, parent = None ):
    super().__init__( parent )
    self._tree = tree

    self._indices = list()

  #-----------------------------------------------------------------------------
  def displayText( self, value, locale ):

    if hasattr( value, 'msg' ):

      text = value.msg

    else:
      text = str(value)

    if len(text) > 80:
      text = text[:80] + "..."

    return text

  #-----------------------------------------------------------------------------
  def paint( self, painter, option, index ):

    if isinstance( index.data(), ModelHint ):

      hint = index.data()

      if hint.level in LEVEL_COLORS:
        path = QtGui.QPainterPath()
        path.addRoundedRect( option.rect, 4, 4 )

        painter.fillPath(
          path,
          LEVEL_COLORS[ hint.level ] )

    return super().paint( painter, option, index )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintWidget ( QtWidgets.QWidget ):

  COL_MSG = 0
  NUM_COLS = 1

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    level = 'debug' ):

    super().__init__()

    self._manager = manager
    self._level = None
    self._level_num = 0
    self._tree = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.setFocusPolicy( QtCore.Qt.StrongFocus )


    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self._tree = VariableTree(
      manager = manager,
      ncols = self.NUM_COLS )

    self._delegate = HintDeligate( tree = self._tree )

    self._tree.setItemDelegate(
      self._delegate )

    self._tree.setExpandsOnDoubleClick( True )

    self.layout.addWidget( self._tree )

    self._top_hints = list()

    self.level = level


    self._ctx_menu = QtWidgets.QMenu(self)

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Copy",
      self,
      statusTip="Copy",
      triggered = self.on_copy ) )

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Copy All",
      self,
      statusTip="Copy All",
      triggered = self.on_copy_all ) )

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Expand Errors",
      self,
      statusTip="Expand All",
      triggered = self.on_expand_errors ) )

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Expand All",
      self,
      statusTip="Expand All",
      triggered = self.on_expand_all ) )

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Collapse All",
      self,
      statusTip="Collapse All",
      triggered = self.on_collapse_all ) )

    self._tree.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
    self._tree.customContextMenuRequested.connect( self.on_context_menu )

  #-----------------------------------------------------------------------------
  @property
  def level( self ):
    return self._level

  #-----------------------------------------------------------------------------
  @level.setter
  def level( self, level ):

    if level != self._level:
      self._level = level
      self._level_num = hint_level_num( level )

      self.rebuild_tree()

  #-----------------------------------------------------------------------------
  def add_hint( self, hint ):
    self._top_hints.append( hint )

    fltr_hints = ModelHint.filter( hint, level = self.level )

    for hint in fltr_hints:
      self.build_hint( hint )

  #-----------------------------------------------------------------------------
  def build_hint( self, hint, parent = None, max_lvl = -1 ):

    if parent is None:
      parent = self._tree


    item = VariableTreeItem( parent = parent )
    item.setData( self.COL_MSG, QtCore.Qt.DisplayRole, hint )

    if hint.loc != '':
      loc_item = VariableTreeItem( parent = item )
      loc_item.setData( self.COL_MSG, QtCore.Qt.DisplayRole, hint.loc )

    item._hint = hint

    p_max_lvl = max( max_lvl, hint.level_num )
    _max_lvl = -1

    for h in hint.hints:
      _max_lvl = max( _max_lvl, self.build_hint(
        hint = h,
        parent = item,
        max_lvl = p_max_lvl ) )

    expand = max_lvl != -1 and (
      _max_lvl > hint.level_num
      or _max_lvl == p_max_lvl
      or hint.level_num == max_lvl )

    item.setExpanded( expand )

    return max( _max_lvl, hint.level_num )

  #-----------------------------------------------------------------------------
  def clear_tree( self, parent = None ):
    if parent is None:
      if self._tree is None:
        return

      for i in range( self._tree.topLevelItemCount()-1, -1, -1 ):
        item = self._tree.topLevelItem(i)
        self.clear_tree( parent = item )

        item.setData( self.COL_MSG, QtCore.Qt.DisplayRole, None )

        if hasattr( item, '_hint' ):
          item._hint = None

        item = None
        self._tree.takeTopLevelItem( i )

    else:
      for i in range( parent.childCount()-1, -1, -1 ):
        item = parent.child(i)
        self.clear_tree( parent = item )

        item.setData( self.COL_MSG, QtCore.Qt.DisplayRole, None )

        if hasattr( item, '_hint' ):
          item._hint = None

        parent.removeChild( item )

        item = None


  #-----------------------------------------------------------------------------
  def rebuild_tree( self ):

    if len(self._top_hints) == 0:
      return

    self.clear_tree()

    for hint in self._top_hints:
      fltr_hints = ModelHint.filter( hint, level = self.level )

      for hint in fltr_hints:
        self.build_hint( hint )

  #-----------------------------------------------------------------------------
  def close( self ):
    self.clear_tree()

  #-----------------------------------------------------------------------------
  def on_context_menu( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_copy( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_copy_all( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_expand_errors( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_expand_all( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_collapse_all( self ):
    pass
