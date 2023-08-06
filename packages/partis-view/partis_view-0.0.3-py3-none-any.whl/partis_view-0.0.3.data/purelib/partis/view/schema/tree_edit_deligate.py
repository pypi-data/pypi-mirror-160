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
  EditLabel,
  rgba )

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

from .tree_edit_node import (
  TreeEditNode )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditDeligate( QtWidgets.QStyledItemDelegate ):

  def __init__( self, tree, parent = None ):
    super().__init__( parent )
    self._tree = tree

    self._indices = list()
    self._editors = list()

  #-----------------------------------------------------------------------------
  # def displayText( self, value, locale ):
  # NOTE: implemented in initStyleOption
  #-----------------------------------------------------------------------------
  def get_text( self, node, col ):
    text = ""

    if col == node.COL_KEY:
      text = node.key

    elif col == node.COL_EDIT:
      text = node.display_text()

    if text is None:
      text = ""

    if len(text) > 80:
      # for whatever reason, Qt has a big performance hit if large text is passed
      # here, and is more efficient to truncate manually
      text = text[:80] + "..."

    return text

  #-----------------------------------------------------------------------------
  def initStyleOption( self, option, index ):
    node = index.data()
    col = index.column()

    if isinstance( node, TreeEditNode ):
      option.text = self.get_text( node, col )

    else:
      super().initStyleOption( option, index )

  #-----------------------------------------------------------------------------
  def createEditor( self, parent, option, index ):
    node = index.data()

    if not (
      isinstance( node, TreeEditNode )
      and index.column() == node.COL_EDIT ):
      return None


    editor = node.build_editor( parent = parent, full = False )
    if editor is None:
      return None

    editor.setAutoFillBackground(True)
    editor.setAttribute( QtCore.Qt.WA_NoMousePropagation, True )

    self._indices.append( index )
    self._editors.append( editor )

    return editor

  #-----------------------------------------------------------------------------
  def destroyEditor( self, editor, index ):
    try:
      i = self._editors.index( editor )
      self._indices.pop( i )
      self._editors.pop( i )

    except:
      pass

    # esures set focus to the tree when editor is destroyed
    self._tree.setFocus()

    return super().destroyEditor( editor, index )

  #-----------------------------------------------------------------------------
  def close_editors( self ):

    for editor in self._editors:
      self.commitData.emit( editor )
      self.closeEditor.emit( editor, QtWidgets.QAbstractItemDelegate.SubmitModelCache )

  #-----------------------------------------------------------------------------
  def setEditorData( self, editor, index ):
    editor.set_state( index.data().get_state_editor( full = False ) )

  #-----------------------------------------------------------------------------
  def setModelData( self, editor, model, index ):
    index.data().set_state_editor( state = editor.state, full = False  )

  #-----------------------------------------------------------------------------
  def updateEditorGeometry( self, editor, option, index ):
    rect = option.rect

    #TODO: see if code editor can take up more room within tree panel
    size = editor.sizeHint()

    if rect.width() < size.width():
       rect.setWidth( size.width() )

    if rect.height() < size.height():
      rect.setHeight( size.height() )

    editor.setGeometry( rect )

  #-----------------------------------------------------------------------------
  def sizeHint( self, option, index ):
    node = index.data()
    col = index.column()

    if isinstance( node, TreeEditNode ):
      # NOTE: since the value is not string, must compute the actual size
      text = self.get_text( node, col )
      document = QtGui.QTextDocument(text)
      document.setDefaultFont(option.font)

      em = option.fontMetrics.height()
      return QtCore.QSize(
        # NOTE: this adds a little to account for padding up to 0.5em.
        # If padding exceeds 0.5, then the text will become truncated
        document.idealWidth() + em,
        # additional to account for any border effect
        em + 2)

    return super().sizeHint( option, index )

  #-----------------------------------------------------------------------------
  def editorEvent( self, event, model, option, index ):
    return super().editorEvent( event, model, option, index )

  #-----------------------------------------------------------------------------
  def eventFilter( self, editor, event ):

    if isinstance( event, QtGui.QKeyEvent ) and event.key() == QtCore.Qt.Key_Escape:
      # overrides default where data would *not* be committed
      self.commitData.emit( editor )
      self.closeEditor.emit( editor, QtWidgets.QAbstractItemDelegate.SubmitModelCache )
      return True

    if isinstance( event, QtGui.QHoverEvent ):
      return True

    if isinstance( event, QtGui.QMouseEvent ):
      return True

    if isinstance( event, QtGui.QHelpEvent ):
      return True

    ret = super().eventFilter( editor, event )

    return ret

  #-----------------------------------------------------------------------------
  def paint( self, painter, option, index ):

    node = index.data()

    if isinstance( node, TreeEditNode ):
      bg_color = node.bg_color( index.column() )

      if bg_color is not None:

        path = QtGui.QPainterPath()
        path.addRoundedRect( option.rect, 4, 4 )

        painter.fillPath(
          path,
          bg_color )

    return super().paint( painter, option, index )
