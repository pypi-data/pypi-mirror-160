# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from pygments import (
  lexers )

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked,
  AsyncTarget )

from partis.view.edit import (
  CodeEdit )

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

from .edit_w import (
  Edit,
  RestrictedEdit )


from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrLineEdit( QtWidgets.QLineEdit ):

  #-----------------------------------------------------------------------------
  def __init__( self, manager, parent = None ):
    super().__init__( parent )

    self._manager = manager

  #-----------------------------------------------------------------------------
  def contextMenuEvent( self, event ):
    event.accept()

    menu = self.createStandardContextMenu()

    filename_act = menu.addAction( "Select File" )
    filename_act.setToolTip( "Set string from file dialog" )

    filename_act.triggered.connect( self.on_select_file )

    dirname_act = menu.addAction( "Select Directory" )
    dirname_act.setToolTip( "Set string from file dialog" )

    dirname_act.triggered.connect( self.on_select_dir )

    menu.exec_( event.globalPos() )


  #-----------------------------------------------------------------------------
  async def file_dialog( self, is_directory = False ):

    target = AsyncTarget()

    dialog = QtWidgets.QFileDialog(self)

    filename = str(self.text())
    fdir = None

    if filename != "":
      dialog.setDirectory( os.path.dirname( filename ) )
    else:
      dialog.setDirectory( os.getcwd() )


    if is_directory:
      dialog.setFileMode(QtWidgets.QFileDialog.Directory )
    else:
      dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)

    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
    dialog.fileSelected.connect( target.on_result )
    dialog.rejected.connect( target.on_result )
    dialog.open()

    result, error = await target.wait()

    if result is not None:
      self.setText( result )

  #-----------------------------------------------------------------------------
  def on_select_file( self ):
    self._manager._manager._async_queue.append( (self.file_dialog, False ) )

  #-----------------------------------------------------------------------------
  def on_select_dir( self ):
    self._manager._manager._async_queue.append( (self.file_dialog, True ) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    # self._line = QtWidgets.QLineEdit()
    self._line = StrLineEdit( manager = self._manager )

    self._line.setReadOnly( self.readonly )

    if self._schema.pattern is not None:
      self._line.setValidator( QtGui.QRegExpValidator(
        self._schema.pattern.pattern ) )

    self._line.editingFinished.connect( self.on_finished_line )

    self._layout.addWidget( self._line )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    with blocked( self._line ):
      self._line.setText( str(state) )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._line.setEnabled( enabled )


  #-----------------------------------------------------------------------------
  def on_finished_line( self ):
    self._state = self._schema.decode(
      val = self._line.text(),
      loc = self._loc )

    self.state_changed.emit( self._state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrMultilineEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._multiline = CodeEdit(
      manager = self._manager,
      expanding = False )

    self._multiline.setReadOnly( self.readonly )

    if self._schema.pattern is not None:
      self._multiline.setValidator( QtGui.QRegExpValidator(
        self._schema.pattern.pattern ) )

    self._multiline.textChanged.connect( self.on_finished_multiline )

    self._layout.addWidget( self._multiline )

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    text = str(state)

    try:
      lexer = lexers.guess_lexer( text )

      self._multiline.set_lang( lexer.aliases[0] )
    except:
      pass

    with blocked( self._multiline ):
      self._multiline.setPlainText( text )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._multiline.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_finished_multiline( self ):

    self._state = self._schema.decode(
      val = self._multiline.toPlainText(),
      loc = self._loc )

    self.state_changed.emit( self._state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrTreeEditNode ( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    schema,
    subedit = None,
    **kwargs ):

    subedit = ( schema.max_lines != 1) and ( schema.restricted is None )

    super().__init__(
      schema = schema,
      subedit = subedit,
      **kwargs )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    if self._schema.restricted is not None:
      editor = RestrictedEdit(
        manager = self._manager,
        schema = self._schema,
        parent = parent,
        loc = self._loc,
        readonly = self.readonly )

    elif self._schema.max_lines == 1:
      editor = StrEdit(
        manager = self._manager,
        schema = self._schema,
        parent = parent,
        loc = self._loc,
        readonly = self.readonly )

    else:
      editor = StrMultilineEdit(
        manager = self._manager,
        schema = self._schema,
        parent = parent,
        loc = self._loc,
        readonly = self.readonly )

    return editor

  #----------------------------------------------------------------------------#
  def set_state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val,
        loc = self._loc )

    super().set_state( state )

  #-----------------------------------------------------------------------------
  def display_text(self):

    return f"\"{self.state._encode}\""
