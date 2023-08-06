# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

import os

from partis.utils import (
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.schema import (
  Loc )

from partis.view.base import (
  blocked,
  WidgetStack )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class History:
  def __init__( self, max_len = None ):
    self._max_len = max_len
    self._cur_hist = -1
    self._hist = list()

  #-----------------------------------------------------------------------------
  def current( self ):
    if self._cur_hist < 0:
      return None

    state = self._hist[ self._cur_hist ]

    return state

  #-----------------------------------------------------------------------------
  def clear( self ):
    self._cur_hist = -1
    self._hist = list()

  #-----------------------------------------------------------------------------
  def push( self, state ):
    if ( self._max_len is not None
      and len(self._hist) == self._max_len
      and self._cur_hist > 0 ):

      self._hist.pop(0)
      self._cur_hist -= 1

    self._cur_hist += 1

    if self._cur_hist < len(self._hist):
      # pushing to a re-wound state discards the existing forward states
      self._hist = self._hist[:self._cur_hist]

    self._hist.insert( self._cur_hist, state )

  #-----------------------------------------------------------------------------
  def forward( self ):

    if self._cur_hist == len(self._hist)-1:
      state = None

    else:
      self._cur_hist += 1

      state = self.current()

    return state

  #-----------------------------------------------------------------------------
  def backward( self ):

    if self._cur_hist <= 0:
      state = None

    else:
      self._cur_hist -= 1

      state = self.current()

    return state


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FileEditor ( QtWidgets.QWidget ):
  """Generic editor for a file
  """
  default_readonly = False

  state_changed = QtCore.Signal(object, object)

  loaded = QtCore.Signal(object)
  loaded_backup = QtCore.Signal(object)

  saved = QtCore.Signal(object)
  saved_backup = QtCore.Signal(object)

  closed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    filename = None,
    state = None,
    readonly = None ):

    super().__init__()

    self._manager = manager
    self._state = None
    self._widget_stack = widget_stack

    self._filename = filename
    self._has_changes = False
    self._hist = History( max_len = 100 )
    self._block_hist = False

    self.state = state
    self._readonly = bool(readonly)

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.installEventFilter(self)

  #-----------------------------------------------------------------------------
  @property
  def readonly( self ):
    return self._readonly

  #-----------------------------------------------------------------------------
  @classmethod
  def guess( self, filename ):
    return 0.5

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  @state.setter
  def state( self, state ):
    if state == self._state:
      return

    if not self._block_hist:
      # NOTE: adds new state to history so that an undo -> redo sequence
      # will recover this state
      self._hist.push( state )

    self._state = state

    # set flag here in case events are being blocked
    self._has_changes = True

    self.state_changed.emit( self, self._state )

  #-----------------------------------------------------------------------------
  @property
  def has_changes( self ):
    return self._has_changes

  #-----------------------------------------------------------------------------
  def clear_changes( self ):
    self._has_changes = False

  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    self.state = state

  #-----------------------------------------------------------------------------
  def eventFilter( self, watched, event ):
    if ( event.type() != QtCore.QEvent.KeyPress
      or event.isAutoRepeat() ):
      return False

    seq = QtGui.QKeySequence( event.modifiers() | event.key() )

    state = None

    if seq == QtGui.QKeySequence.Undo:
      state = self._hist.backward()

    elif seq == QtGui.QKeySequence.Redo:
      state = self._hist.forward()

    else:
      return False

    if state is not None:

      self._block_hist = True

      with blocked( self ):
        self.set_state( state )

      self._block_hist = False

    return True

  #-----------------------------------------------------------------------------
  @property
  def filename( self ):
    return self._filename

  #-----------------------------------------------------------------------------
  @filename.setter
  def filename( self, filename ):
    self._filename = filename

  #-----------------------------------------------------------------------------
  @property
  def filename_backup( self ):
    if self._filename is None:
      raise ValueError("Filename has not be set")

    return self._filename + ".bak"

  #-----------------------------------------------------------------------------
  def check_backup( self ):
    """Check whether there is a backup file that is more recent than the save file
    """
    if self.filename is None:
      return False

    path = self.filename
    bak_path = self.filename_backup

    if not os.path.exists( path ) or not os.path.exists( bak_path ):
      return False

    if os.state(path).st_mtime >= os.state(bak_path).st_mtime:
      # if save file is more recent, ignore backup file
      return False

    return True

  #-----------------------------------------------------------------------------
  def close( self ):
    self.closed.emit( self )

  #-----------------------------------------------------------------------------
  def _load( self,
    backup = False,
    binary = False ):
    """Internal load method
    """

    if self._filename is None:
      raise ValueError("Filename has not be set")

    if backup:
      path = self.filename_backup
    else:
      path = self.filename

    if not os.path.exists( path ):
      raise ValueError(f"File not found: {path}")

    if not os.path.isfile( path ):
      raise ValueError(f"Path is not a file: {path}")

    with open( path, 'rb' ) as fp:
      data = fp.read()

    if not binary:
      data = data.decode( 'utf-8', errors = 'replace' )


    loc = Loc(
      filename = path )

    return data, loc

  #-----------------------------------------------------------------------------
  def load( self,
    backup = False ):
    """Load file contents into state
    """

    if backup:
      self.loaded_backup.emit(self)
    else:
      self.loaded.emit(self)

  #-----------------------------------------------------------------------------
  def _save( self,
    data,
    backup = False,
    binary = False ):
    """Internal save method
    """

    if self._filename is None:
      raise ValueError("Filename has not be set")

    if backup:
      path = self.filename_backup
    else:
      path = self.filename

    if not binary:
      data = data.encode( 'utf-8', errors = 'replace' )

    dir, file = os.path.split( path )

    if not os.path.exists( dir ):
      os.makedirs( dir )

    with open( path, 'wb' ) as fp:
      fp.write( data )

  #-----------------------------------------------------------------------------
  def save( self,
    backup = False ):
    """Save state to file
    """

    if backup:
      self.saved_backup.emit(self)
    else:
      self.saved.emit(self)

    self._has_changes = False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextFileEditor( FileEditor ):
  #-----------------------------------------------------------------------------
  def load( self, backup = False ):

    self._hist.clear()
    self.clear_changes()

    src, loc = self._load(
      backup = backup,
      binary = False )

    self.set_state( src )
    self.clear_changes()

    super().load( backup = backup )

  #-----------------------------------------------------------------------------
  def save( self, backup = False ):
    self._save(
      data = self.state,
      backup = backup,
      binary = False )

    super().save( backup = backup )
