# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import sys
import logging
import time
log = logging.getLogger( __name__ )

from PySide2 import QtCore, QtGui, QtWidgets



from partis.view.base import (
  WidgetStack,
  DirectoryTreeWidget )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DirectoryTabComplete( QtWidgets.QLineEdit ):
  #-----------------------------------------------------------------------------
  def __init__( self,
    manager ):
    super().__init__( )

    self._manager = manager
    self._last_time = time.monotonic() - 10.0
    self._hist = list()

  #-----------------------------------------------------------------------------
  def event(self,event):
    if event.type() == QtCore.QEvent.KeyPress:
      fwd = event.key() == QtCore.Qt.Key_Tab
      bwd = event.key() == QtCore.Qt.Key_Backtab

      seq = QtGui.QKeySequence( event.modifiers() | event.key() )
      undo = seq == QtGui.QKeySequence.Undo

      if fwd or bwd:
        cur_time = time.monotonic()
        dt = cur_time - self._last_time
        self._last_time = cur_time

        if bwd or dt <= 0.5:
          self.tab_next(
            bwd = bwd )
        else:
          self.tab_complete()

        return True

      if undo and len(self.hist) > 0:
        self.path = self.hist[-1]
        return True

    return QtWidgets.QLineEdit.event( self, event )

  #-----------------------------------------------------------------------------
  @property
  def hist( self ):
    return self._hist

  #-----------------------------------------------------------------------------
  @property
  def path( self ):
    return self.text()

  #-----------------------------------------------------------------------------
  @path.setter
  def path( self, path ):
    if self.path == path:
      # already set
      return

    if len(self.hist) > 0:
      if self.hist[-1] == path:
        # setting to the previous path
        self.hist.pop()
      elif self.path != '':
        # setting to new path
        self.hist.append( self.path )

    elif self.path != '':
      # setting to new path
      self.hist.append( self.path )

    self.setText( path )

  #-----------------------------------------------------------------------------
  def tab_complete( self ):
    cur = self.path

    dir, base = os.path.split( cur )
    _base = base.lower()

    # names = [ f
    #   for f in os.listdir( dir )
    #   if os.path.isdir( os.path.join(dir, f) ) ]

    names = os.listdir( dir )

    _names = [ f.lower() for f in names ]

    pairs = [ (f, _f) for f, _f in zip(names, _names) if _f.startswith(_base) ]

    opts = sorted( pairs,
      key = lambda p: p[1] )

    if len(opts) == 0:
      return

    path = os.path.join( os.path.join( dir, opts[0][0] ) )

    self.path = path

  #-----------------------------------------------------------------------------
  def tab_next(self, bwd = False ):
    cur = self.path

    dir, base = os.path.split( cur )

    # opts = sorted([ f
    #   for f in os.listdir( dir )
    #   if os.path.isdir( os.path.join(dir, f) ) ],
    #   key = lambda f: f.lower() )

    opts = sorted( os.listdir( dir ),
      key = lambda f: f.lower() )

    n = len(opts)

    if n == 0:
      return

    # find entry that is next in the sorted sequence
    if bwd:
      i = n-1

      while i >= 0 and opts[ i ].lower() >= base.lower():
        i -= 1

      if i < 0:
        i = n-1

    else:
      i = 0

      while i < n and opts[ i ].lower() <= base.lower():
        i += 1

      if i >= n:
        i = 0

    path = os.path.join( os.path.join( dir, opts[ i ] ) )

    self.path = path


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkDirWidget ( QtWidgets.QWidget ):
  """Widget to manage files in the working directory
  """

  file_open = QtCore.Signal(str)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    root_dir = None ):
    super().__init__( )

    self._manager = manager
    self._state = None


    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self._root_dir = DirectoryTabComplete(
      manager = self._manager )

    self._root_dir.editingFinished.connect( self.on_finished_root_dir )

    self.files = DirectoryTreeWidget()
    self.files.file_double_clicked.connect( self.file_open )

    self.files.dir_change.connect( self.set_root_dir )

    self.editors = QtWidgets.QTabWidget()

    self.layout.addWidget( self._root_dir )
    self.layout.addWidget( self.files )

    self.set_root_dir( root_dir = root_dir )

  #-----------------------------------------------------------------------------
  @property
  def root_dir( self ):
    return self._root_dir.path

  #-----------------------------------------------------------------------------
  @root_dir.setter
  def root_dir( self, root_dir ):
    self.set_root_dir( root_dir = root_dir )

  #-----------------------------------------------------------------------------
  def set_root_dir( self, root_dir ):

    if self.files.model() is None:
      # sometimes this might be called after model has been destroyed
      return

    if root_dir is None:
      root_dir = QtCore.QDir.currentPath()

    if not os.path.exists( root_dir ):
      return

    root_dir = os.path.abspath( root_dir )

    if os.path.isfile( root_dir ):
      self.file_open.emit( root_dir )

      root_dir, name = os.path.split( root_dir )

    if not os.path.isdir( root_dir ):
      return

    self._root_dir.path = str(root_dir)

    self.files.model().setRootPath( root_dir )
    self.files.setRootIndex( self.files.model().index( root_dir ) )

  #-----------------------------------------------------------------------------
  def set_state( self, next_state ):
    if next_state is self._state:
      return

    self._state = next_state

  #-----------------------------------------------------------------------------
  def on_finished_root_dir( self ):
    self.set_root_dir( root_dir = self._root_dir.path )

  #-----------------------------------------------------------------------------
  def on_item_double_clicked( self, item, col ):
    pass
