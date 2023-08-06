# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import sys
import trio

from PySide2 import QtCore, QtGui, QtWidgets

from partis.utils import (
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.schema.serialize.yaml import (
  dumps )

from partis.view.base import (
  WidgetStack,
  AsyncTarget )

from .workdir import WorkDirWidget

from .select_editor import (
  SelectEditorDialog )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Project( QtWidgets.QWidget ):
  """The whole project
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    editor_map,
    root_dir = None ):
    super().__init__( )

    self._manager = manager
    self._state = None
    self._editor_map = editor_map
    self._editors = list()
    # self._editor_stacks = list()


    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.splitter = QtWidgets.QSplitter( self )
    self.layout.addWidget( self.splitter )

    self.workdir = WorkDirWidget(
      manager = self._manager,
      root_dir = root_dir )

    self.workdir.file_open.connect( self.on_open_editor )

    self.editor_tabs = QtWidgets.QTabWidget()
    self.editor_tabs.setTabsClosable( True )
    self.editor_tabs.tabCloseRequested.connect( self.on_close_editor )

    self.splitter.insertWidget( 0, self.workdir )
    self.splitter.insertWidget( 1, self.editor_tabs )

    width = QtWidgets.QApplication.instance().desktop().availableGeometry(self).width()
    self.splitter.setSizes([width * 0.25, width * 0.75])

    # self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    # self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #-----------------------------------------------------------------------------
  def current_index( self ):
    if len(self._editors) == 0:
      return None

    return self.editor_tabs.currentIndex()

  #-----------------------------------------------------------------------------
  def editor( self, editor = None ):
    if isinstance( editor, int ):
      editor = self._editors[ editor ]

    if editor is None:
      index = self.current_index()

      if index is None:
        editor = None
      else:
        editor = self._editors[ index ]

    return editor

  #-----------------------------------------------------------------------------
  def set_root_dir( self, root_dir ):

    self.workdir.root_dir = root_dir

  #-----------------------------------------------------------------------------
  def set_state( self, next_state ):
    if next_state is self._state:
      return

    self._state = next_state

  #-----------------------------------------------------------------------------
  async def close( self ):
    while len(self._editors) > 0:
      await self.close_editor( allow_cancel = False )

  #-----------------------------------------------------------------------------
  async def save_editor_as( self, editor = None ):
    editor = self.editor( editor )

    if editor is None:
      return

    target = AsyncTarget()

    save_dialog = QtWidgets.QFileDialog(self)

    save_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    save_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    save_dialog.fileSelected.connect( target.on_result )
    save_dialog.rejected.connect( target.on_result )
    save_dialog.open()

    result, error = await target.wait()

    if result is not None:
      editor.filename = result

      editor.save()

  #-----------------------------------------------------------------------------
  async def save_editor( self, editor = None ):

    editor = self.editor( editor )

    if editor is None:
      return

    if editor.filename is None:
      await self.save_editor_as()

    else:
      editor.save()

  #-----------------------------------------------------------------------------
  async def close_editor( self, editor = None, allow_cancel = True ):

    editor = self.editor( editor )

    if editor is None:
      return

    if editor.has_changes:
      target = AsyncTarget()

      if editor.filename is not None:
        name = editor.filename
      else:
        name = 'untitled'

      message_box = QtWidgets.QMessageBox()
      message_box.setWindowTitle( f"Closing '{name}'" )
      message_box.setWindowIcon( QtGui.QIcon(self._manager.resource_path("images/icons/app_icon.png")) )
      message_box.setStyleSheet( self._manager.stylesheet )
      message_box.setText(
        f"Closing editor with changes for '{name}'.")

      if allow_cancel:
        message_box.setStandardButtons(
          QtWidgets.QMessageBox.Save
          | QtWidgets.QMessageBox.Cancel
          | QtWidgets.QMessageBox.Discard )

      else:
        message_box.setStandardButtons(
          QtWidgets.QMessageBox.Save
          | QtWidgets.QMessageBox.Discard )

      message_box.setDefaultButton( QtWidgets.QMessageBox.Save )


      message_box.finished.connect( target.on_result )
      message_box.open()

      result, error = await target.wait()

      if result == QtWidgets.QMessageBox.Cancel:
        return

      elif result == QtWidgets.QMessageBox.Save:

        await self.save_editor( editor )

      # discard -> simply close editor

    editor.close()

    index = self._editors.index( editor )
    self.editor_tabs.removeTab( index )
    self._editors.pop( index )

  #-----------------------------------------------------------------------------
  async def open_editor( self,
    filename = None,
    editor_class = None,
    readonly = None ):

    if editor_class is None:

      if filename is None:
        title = f"Select Editor for 'untitled'"
      else:
        title = f"Select Editor for '{filename}'"

      target = AsyncTarget()

      select_dialog = SelectEditorDialog(
        title = title,
        manager = self._manager,
        editors = self._editor_map.editors )

      if filename is not None:
        select_dialog.guess_editor( filename )

      select_dialog.accepted.connect( target.on_result )
      select_dialog.rejected.connect( target.on_result )
      select_dialog.open()

      result, error = await target.wait()

      editor_class = select_dialog.selected
      readonly = select_dialog.readonly

    if editor_class is not None:

      return self.add_editor(
        editor_class = editor_class,
        filename = filename,
        readonly = readonly )


    return None

  #-----------------------------------------------------------------------------
  def add_editor( self,
    editor_class,
    state = None,
    readonly = None,
    filename = None ):

    if filename is not None:

      filename = os.path.abspath( filename )

      dir, name = os.path.split(filename)

    else:
      name = "untitled"

    widget_stack = WidgetStack(
      manager = self._manager )

    # self._editor_stacks.append( widget_stack )

    load_failed = False

    editor = editor_class(
      manager = self._manager,
      widget_stack = widget_stack,
      state = state,
      filename = filename,
      readonly = readonly )

    editor.clear_changes()

    if filename is not None:
      if os.path.exists( filename ):
        try:
          editor.load()

        except Exception as e:
          self._manager.show_exception(
            title = f"Error loading {filename}",
            exc = e )

          log.error( ModelHint.cast(e) )

          load_failed = True


    self.editor_tabs.addTab(
      widget_stack,
      name )

    self._editors.append( editor )

    self.editor_tabs.setCurrentIndex( len(self._editors)-1 )

    widget_stack.push_widget( editor )

    if load_failed:
      # TODO: surely there is a better way to do this. The problem is if the widgets
      # are never added to any parent it seems to eventually cause a seg. fault.
      # Clearly a bug in Qt/Python memory management confict, but this seems to work ok
      self.on_close_editor( editor = editor, allow_cancel = False )

      return None

    return editor

  #-----------------------------------------------------------------------------
  def on_open_editor( self, filename = None, editor_class = None ):
    self._manager._manager._async_queue.append( ( self.open_editor, filename, editor_class ) )

  #-----------------------------------------------------------------------------
  def on_save_editor( self, editor = None ):
    self._manager._manager._async_queue.append( (self.save_editor, editor) )

  #-----------------------------------------------------------------------------
  def on_save_editor_as( self, editor = None ):
    self._manager._manager._async_queue.append( (self.save_editor_as, editor) )

  #-----------------------------------------------------------------------------
  def on_close_editor( self, editor = None, allow_cancel = True ):
    self._manager._manager._async_queue.append( (self.close_editor, editor, allow_cancel ) )

  #-----------------------------------------------------------------------------
  def on_close( self ):
    self._manager._manager._async_queue.append( (self.close, ) )

  #-----------------------------------------------------------------------------
  async def test_project_editors( self ):

    await self._test_project_editors( self._editor_map.editors )

  #-----------------------------------------------------------------------------
  async def _test_project_editors( self, editors ):
    for i, (editor_name, editor_class) in enumerate( editors.items() ):

      log.info(f"testing editor: {editor_name}")

      if isinstance( editor_class, dict ):
        return _test_project_editors( editor_class )

      editor = await self.open_editor(
        filename = f"test_{i}.txt",
        editor_class = editor_class )

      assert( editor is not None )

      self._manager._manager.test( editor )
