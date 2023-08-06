# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import trio
import time
import logging
log = logging.getLogger( __name__ )

from PySide2 import QtCore, QtGui, QtWidgets


from partis.utils import (
  ModelHint )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class blocked:
  #-----------------------------------------------------------------------------
  def __init__(self, *objs ):
    self._objs = objs
    self._prev = [None for obj in self._objs]

  #-----------------------------------------------------------------------------
  def __enter__(self):
    for i, obj in enumerate(self._objs):
      self._prev[i] = obj.blockSignals( True )

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):
    for i, obj in enumerate(self._objs):
      obj.blockSignals( self._prev[i] )

    # do not handle any exceptions here
    return False

#-----------------------------------------------------------------------------
def rgba( r, g = None, b = None, a = None ):
  """Converts RGBA values to a QColor with a function signiture similar to the
  CSS ``rgba()`` functional representation.

  .. note::

    A single string argument may also be used in the hex format ``RRGGBBAA``
    or ``RGBA``.

  Parameters
  ----------
  r : int | str
    0-255, '#RGBA', or '#RRGGBBAA'
  g : int | None
    0-255 | None
  b : int | None
    0-255
  a : float | None
    0.0-1.0
  """

  is_rgba = all([r,g,b,a])
  is_hex = isinstance(r, str) and not any([g,b,a])

  if not( is_rgba or is_hex ):
    raise ValueError(
      "Arguments must either be a single string in '#RRGGBBAA' hex format, or separate r,g,b,a components:"
      f" r = {r}, g = {g}, b = {b}, a = {a}")

  if is_hex:
    hex = r

    assert len(hex) > 0

    if hex[0] == '#':
      hex = hex[1:]

    if len(hex) == 4:
      r = int(hex[0], base = 16)
      g = int(hex[1], base = 16)
      b = int(hex[2], base = 16)
      a = int(hex[2], base = 16)

    elif len(hex) == 8:
      r = int(hex[:2], base = 16)
      g = int(hex[2:4], base = 16)
      b = int(hex[4:6], base = 16)
      a = int(hex[6:8], base = 16)

    else:
      assert False, f"hex format not valid: {hex}"

  else:
    r = int(r)
    g = int(g)
    b = int(b)
    a = int( round(float(a) * 255) )

  qcolor = QtGui.QColor( r, g, b, a )

  # qcolor.setRgb( r, g, b, a )

  return qcolor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolButton( QtWidgets.QToolButton ):
  def __init__( self, icon_path, tooltip, parent = None ):
    super(ToolButton, self).__init__(parent)

    self.setIcon( QtGui.QIcon(icon_path) )
    self.setToolTip(tooltip)
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ClickLabel( QtWidgets.QLabel, QtWidgets.QWidget ):

  clicked = QtCore.Signal()
  doubleclicked = QtCore.Signal()
  pressed = QtCore.Signal()
  released = QtCore.Signal()

  #----------------------------------------------------------------------------#
  def __init__( self, text ):
    super(ClickLabel, self).__init__(text)

  #----------------------------------------------------------------------------#
  def mousePressEvent( self, event ):
    super().mousePressEvent( event )

    self.clicked.emit()
    self.pressed.emit()

  #----------------------------------------------------------------------------#
  def mouseReleaseEvent( self, event ):
    super().mouseReleaseEvent( event )

    self.released.emit()

  #----------------------------------------------------------------------------#
  def mouseDoubleClickEvent( self, event ):
    super().mouseDoubleClickEvent( event )

    self.doubleclicked.emit()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LineEdit( QtWidgets.QLineEdit ):
  focusout = QtCore.Signal()
  #-----------------------------------------------------------------------------
  def focusOutEvent(self, event):
    self.focusout.emit()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ScrollComboBox( QtWidgets.QComboBox ):
  """This is combobox compatible with a scroll area to prevent it from taking
  focus during scrolling.
  The mouse wheel will only change combo index if it already has focus.
  """

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__( *args, **kwargs )

    self.setFocusPolicy( QtCore.Qt.StrongFocus )
    self.readonly = False

  #-----------------------------------------------------------------------------
  def wheelEvent( self, event ):
    if self.readonly or not self.hasFocus():
      event.ignore()
    else:
      super().wheelEvent( event )

  #-----------------------------------------------------------------------------
  def mousePressEvent(self, event):
    if self.readonly:
      event.ignore()
    else:
      super().mousePressEvent( event )

  #-----------------------------------------------------------------------------
  def keyPressEvent(self, event):
    if self.readonly:
      event.ignore()
    else:
      super().keyPressEvent( event )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditLabel( QtWidgets.QWidget ):

  clicked = QtCore.Signal()
  doubleclicked = QtCore.Signal()
  pressed = QtCore.Signal()
  released = QtCore.Signal()
  textChanged = QtCore.Signal(str)

  #----------------------------------------------------------------------------#
  def __init__( self, text ):
    super().__init__()

    self._layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self._layout)

    self._layout.setContentsMargins(0,0,0,0)
    self._layout.setSpacing(0)

    self._label = QtWidgets.QLabel( text )
    self._layout.addWidget( self._label )

    self._line = LineEdit( text )
    self._layout.addWidget( self._line )

    self.clicked.connect( self.show_edit )
    self._line.editingFinished.connect( self.show_label )
    self._line.focusout.connect( self.show_label )
    self._line.textChanged.connect( self.setText )

    self.layout().setSizeConstraint( QtWidgets.QLayout.SetFixedSize )

    self.show_label()

  #----------------------------------------------------------------------------#
  def mousePressEvent( self, event ):
    super().mousePressEvent( event )

    self.clicked.emit()
    self.pressed.emit()

  #----------------------------------------------------------------------------#
  def mouseReleaseEvent( self, event ):
    super().mouseReleaseEvent( event )

    self.released.emit()

  #----------------------------------------------------------------------------#
  def mouseDoubleClickEvent( self, event ):
    super().mouseDoubleClickEvent( event )

    self.doubleclicked.emit()

  #----------------------------------------------------------------------------#
  def show_edit( self, *args ):
    self._label.setVisible( False )
    self._line.setVisible( True )
    self.adjustSize()

  #----------------------------------------------------------------------------#
  def show_label( self, *args ):
    self._label.setVisible( True )
    self._line.setVisible( False )
    self.adjustSize()

  #----------------------------------------------------------------------------#
  def setText( self, text ):
    with blocked( self._line ):
      self._line.setText( text )

    self._label.setText( text )

    self.textChanged.emit( text )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HLine( QtWidgets.QFrame ):
  def __init__(self):
    super( ).__init__()
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.setFrameShape( QtWidgets.QFrame.HLine )
    self.setFrameShadow( QtWidgets.QFrame.Sunken )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Heading1 ( QtWidgets.QLabel ):
  #-----------------------------------------------------------------------------
  def __init__( self, text ):
    super( ).__init__( text )

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Heading2 ( QtWidgets.QLabel ):
  #-----------------------------------------------------------------------------
  def __init__( self, text ):
    super( ).__init__( text )

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Heading3 ( QtWidgets.QLabel ):
  #-----------------------------------------------------------------------------
  def __init__( self, text ):
    super( ).__init__( text )

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ConfigTree ( QtWidgets.QTreeWidget ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DirectoryTreeWidget( QtWidgets.QTreeView ):
  file_clicked = QtCore.Signal(str)
  file_double_clicked = QtCore.Signal(str)

  dir_clicked = QtCore.Signal(str)
  dir_double_clicked = QtCore.Signal(str)

  # request to change to given directory
  dir_change = QtCore.Signal(str)

  #-----------------------------------------------------------------------------
  def __init__( self ):
    super().__init__()

    model = QtWidgets.QFileSystemModel()

    model.setReadOnly(True);

    model.setFilter(
      QtCore.QDir.AllDirs
      | QtCore.QDir.AllEntries
      | QtCore.QDir.NoDotAndDotDot
      | QtCore.QDir.Hidden );

    self.setModel( model )


    self.header().hideSection(1)
    self.header().hideSection(2)
    self.header().hideSection(3)
    self.header().setVisible(False)

    self.clicked.connect( self.on_clicked )
    self.doubleClicked.connect( self.on_double_clicked )

    self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
    self.customContextMenuRequested.connect( self.on_context_menu )

    self._ctx_menu = QtWidgets.QMenu(self)

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Copy Path",
      self,
      statusTip="Copy Path",
      triggered = self.on_copy_path ) )

    self._ctx_menu.addAction( QtWidgets.QAction(
      "Change Directory",
      self,
      statusTip="Change Directory",
      triggered = self.on_change_directory ) )

  #-----------------------------------------------------------------------------
  def on_clicked( self, index ):
    index = self.selectionModel().currentIndex()

    path = self.model().filePath( index )

    if os.path.isfile( path ):
      self.file_clicked.emit( path )

    if os.path.isdir( path ):
      self.dir_clicked.emit( path )

  #-----------------------------------------------------------------------------
  def on_double_clicked( self, index ):

    index = self.selectionModel().currentIndex()

    path = self.model().filePath( index )

    if os.path.isfile( path ):
      self.file_double_clicked.emit( path )

    if os.path.isdir( path ):
      # if os.path.samefile( path, os.path.join( self.model().rootPath(), os.pardir ) ):
      #   # if parent directory double clicked, instead signal to change to parent directory
      #   self.dir_change.emit( path )
      #
      # else:

      self.dir_double_clicked.emit( path )

  #-----------------------------------------------------------------------------
  def on_context_menu( self, pos ):

    self._ctx_menu.exec_( self.viewport().mapToGlobal(pos) )

  #-----------------------------------------------------------------------------
  def on_copy_path( self ):
    index = self.selectionModel().currentIndex()

    path = self.model().filePath( index )

    cb = QtWidgets.QApplication.instance().clipboard()

    # global clipboard.
    cb.setText( path, QtGui.QClipboard.Clipboard )

    if cb.supportsSelection():
      # global mouse selection clipboard, if supported
      cb.setText( path, QtGui.QClipboard.Selection )

    time.sleep(0.001)

  #-----------------------------------------------------------------------------
  def on_change_directory( self ):

    index = self.selectionModel().currentIndex()

    path = self.model().filePath( index )

    self.dir_change.emit( path )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class QtLogHandler:
  #-----------------------------------------------------------------------------
  def __init__( self, logger ):
    self._logger = logger

  #-----------------------------------------------------------------------------
  def qt_message_handler( self,
    msg_type,
    context,
    msg ):

    level = {
      QtCore.QtDebugMsg: logging.DEBUG,
      QtCore.QtInfoMsg: logging.INFO,
      QtCore.QtWarningMsg: logging.WARNING,
      QtCore.QtCriticalMsg: logging.ERROR,
      QtCore.QtFatalMsg: logging.CRITICAL }[ msg_type ]

    loc = ""

    if context.file is not None:
      loc += f"file: {context.file}"

    if context.line is not None:
      loc += f" line:{context.line}"

    if context.function is not None:
      loc += f" function:{context.function}"

    hints = list()

    hint = ModelHint(
      msg = msg,
      loc = loc,
      level = level,
      hints = hints )


    self._logger.log( level, hint )
