# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from .edit import (
  Project,
  editor_map )

from datetime import datetime
import sys
import os
import re
from timeit import default_timer as timer
import time
import math

import logging
from partis.utils import (
  f,
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.view.base import (
  AsyncTarget )

from partis.view.dialog import (
  LogDialog )

# this is only needed for Qt 5 on Mac OS
os.environ['QT_MAC_WANTS_LAYER'] = '1'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MainWindow ( QtWidgets.QMainWindow ):
  """Main application window
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    theme,
    logger = None ):
    super( ).__init__()

    if logger is None:
      logger = log

    self._logger = logger
    self._manager = manager
    self._closed = False
    self._is_full_screen = False

    self.restore_time = None
    self.restore_save_file = None
    self.restore_buf = None

    self.restore_point_wait = 2
    self.last_restore_point_time = None

    self._prev_state = None

    self.init = True

    self._theme = None
    self._theme_module = None
    self._theme_rcc = None
    self._resource_dir = None
    self.stylesheet = ""
    # self.font_db = QtGui.QFontDatabase()

    # self._px_per_ex = self.fontMetrics().xHeight()
    self._px_per_ex = float(self.fontMetrics().width('9'))
    self._px_per_em = float(self.fontMetrics().width('9'))
    self._px_per_pt = float(self.fontMetrics().width('40') / 40)

    if theme is not None:
      self.set_theme( theme )
    else:
      self.set_theme( "light" )

    self.setWindowTitle("partis")

    # system configuration menu
    self.project = Project(
      manager = self,
      editor_map = editor_map )

    self.setCentralWidget( self.project )

    self.readSettings()
    self.createActions()
    self.createMenus()
    self.createToolBars()
    self.createStatusBar()

    self.setUnifiedTitleAndToolBarOnMac(True)

  #----------------------------------------------------------------------------#
  def dispatch( self, action ):
    self._manager.dispatch( action )

  #-----------------------------------------------------------------------------
  @property
  def state(self):
    return self._manager.state

  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    if self._prev_state is state:
      return

    self.project.set_state( state )

    timestamp = timer()

    if self.last_restore_point_time is None or self.last_restore_point_time - timestamp > self.restore_point_wait:
      self.last_restore_point_time = timestamp
      self.writeSettings()

    self._prev_state = state

  #-----------------------------------------------------------------------------
  async def async_close( self ):
    # self.writeSettings()
    # self._manager.dispatch( njm.actions.system.Shutdown() )
    await self.project.close()

    self._closed = True

    self.close()

  #-----------------------------------------------------------------------------
  def closeEvent( self, event ):
    if self._closed:
      event.accept()
      self._manager.exit()
      return

    self._manager._async_queue.append( (self.async_close, ) )

  #-----------------------------------------------------------------------------
  def newState (self):
    self.project.on_open_editor()

  #-----------------------------------------------------------------------------
  def loadState (self):
    dialog = QtWidgets.QFileDialog(self)
    dialog.setDirectory( self.project.workdir.root_dir )
    dialog.setFileMode(QtWidgets.QFileDialog.AnyFile )
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

    dialog.fileSelected.connect( self.loadStateFinish )
    dialog.open()

  #-----------------------------------------------------------------------------
  def open_dir (self):
    dialog = QtWidgets.QFileDialog(self)
    dialog.setDirectory( self.project.workdir.root_dir )
    dialog.setFileMode(QtWidgets.QFileDialog.Directory )
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

    dialog.fileSelected.connect( self.loadStateFinish )
    dialog.open()

  #-----------------------------------------------------------------------------
  def loadStateFinish (self, file):
    if file is not None and file != "":
      if os.path.isfile( file ):
        self.project.on_open_editor( file )

      elif os.path.isdir( file ):
        self.project.set_root_dir( file )

  #-----------------------------------------------------------------------------
  def saveState (self):

    self.project.on_save_editor()

  #-----------------------------------------------------------------------------
  def saveStateAs (self):
    self.project.on_save_editor_as()


  #-----------------------------------------------------------------------------
  def restorePoint( self ):
    if self.restore_buf is not None:
      self.unpack_app( self.restore_buf )

    self._save_file = self.restore_save_file



    if self._save_file is not None:
      self.saveAct.setText("&Save ({})".format(os.path.basename(self._save_file)) )


  #-----------------------------------------------------------------------------
  def about(self):

    try:
      import pkg_resources
      version = pkg_resources.get_distribution("partis").version
    except:
      version = ""

    QtWidgets.QMessageBox.about(self, "About partis",
      "partis\n"
      f"version: {version}\n\n"
      "")

  #-----------------------------------------------------------------------------
  def documentWasModified(self):
    #self.setWindowModified(self.textEdit.document().isModified())
    pass

  #-----------------------------------------------------------------------------
  def config_system( self ):
    self.system.show()
    getattr(self.system, 'raise')()
    self.system.activateWindow()

  #-----------------------------------------------------------------------------
  def createActions(self):

      # TODO: set icons in set_theme method
      self.newAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/new.svg')),
        "&New File",
        self,
        shortcut=QtGui.QKeySequence.New,
        statusTip="Create a new file",
        triggered=self.newState )

      self.openAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/load.svg')),
        "&Open File",
        self,
        shortcut=QtGui.QKeySequence.Open,
        statusTip="Open a file",
        triggered=self.loadState )

      self.openDirAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/load.svg')),
        "&Open Folder",
        self,
        shortcut=QtGui.QKeySequence("Ctrl+Shift+O"),
        statusTip="Open a directory",
        triggered=self.open_dir )

      self.saveAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/save.svg')),
        "&Save", self,
        shortcut=QtGui.QKeySequence.Save,
        statusTip="Save state to disk",
        triggered=self.saveState )
      #
      self.saveAsAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/saveAs.svg')),
        "Save &As...",
        self,
        shortcut=QtGui.QKeySequence("Ctrl+Shift+S"),
        statusTip="Save the document under a new name",
        triggered=self.saveStateAs)

      self.restoreAct = QtWidgets.QAction(
        QtGui.QIcon(self.resource_path('images/icons/restore.svg')),
        "Restore Point ({})".format(datetime.fromtimestamp(self.restore_time) if self.restore_time else None),
        self,
        statusTip="Restore application to previous restore point.",
        triggered=self.restorePoint)


      self.exitAct = QtWidgets.QAction("E&xit",
        self,
        shortcut="Ctrl+Q",
        statusTip="Exit the application",
        triggered=self.close)


      self.aboutAct = QtWidgets.QAction("&About",
        self,
        statusTip="Show the application's About box",
        triggered=self.about)

      self.window_act = QtWidgets.QAction(
        "Full-Screen",
        self, shortcut="F11",
        statusTip="Window mode",
        triggered=self.on_window_mode )


  #-----------------------------------------------------------------------------
  def createMenus(self):
      self.fileMenu = self.menuBar().addMenu("&File")
      self.fileMenu.addAction(self.newAct)
      self.fileMenu.addAction(self.openAct)
      self.fileMenu.addAction(self.openDirAct)
      self.fileMenu.addAction(self.saveAct)
      self.fileMenu.addAction(self.saveAsAct)
      self.fileMenu.addAction(self.restoreAct)
      self.fileMenu.addSeparator()
      self.fileMenu.addAction(self.exitAct)
      #

      self.menuBar().addAction(self.window_act)

      # self.menuBar().addSeparator()

      self.helpMenu = self.menuBar().addMenu("&Help")
      self.helpMenu.addAction(self.aboutAct)

  #-----------------------------------------------------------------------------
  def createToolBars(self):
      # self.fileToolBar = self.addToolBar("Operations")
      # self.fileToolBar.addAction(self.newAct)
      # self.fileToolBar.addAction(self.openAct)
    pass

  #-----------------------------------------------------------------------------
  def createStatusBar(self):
      self.statusBar().showMessage("Ready")

  #-----------------------------------------------------------------------------
  def unpack_app( self, buf ):

    app_state = njm.unpack( buf )

    state = app_state["state"]

    configs_changed = []

    state = njm.config.base.fixup_config(
      types = self._types,
      state = state,
      changed = configs_changed )

    state.update_paths()

    # ensure loading previous state does not throw system into undefined configuration
    # current MPI ranks
    cur_ranks = self.state.get('status').keys()

    # overwrite save rank statuses
    new_state = state.update( "status", njm.base.State("", { k : njm.config.Status.INIT for k in cur_ranks }) )

    # remove logs from saved file
    new_state = new_state.update( "log", njm.base.State("", {}) )


    channels_changed = []

    # remove any channels not currently supported
    for c in new_state['channels'].keys():
      if int(c) >= self._nchannel:
        new_state = new_state.delete(f'channels/{c}')
        channels_changed.append(f'deleted: channels/{c}')

    # add entry for channels not in saved state
    for c in range(self._nchannel):
      c = str(c)

      if c not in new_state['channels']:
        new_state = new_state.update( f'channels/{c}', njm.config.channel.Channel.default() )
        channels_changed.append(f'added: channels/{c}')



    # force gui elements to update immediatly so that layout can be restored
    self.set_state( new_state )

    for i in new_state["gui"]["grid_view"].keys():
      self.grid_view[int(i)].restore_layout( app_state["layout"][i] )

    non_gui_state = dict(new_state)
    non_gui_state.pop('gui')

    # update central state to propagate changes naturally to any other elements
    self._manager.dispatch( njm.actions.Update("", non_gui_state ) )
    self._manager.dispatch_gui( njm.actions.Update("gui", app_state["state"]["gui"] ) )

    # dispatch warnings after state update so they will appear
    #...........................................................................
    if len(configs_changed) > 0:
      self.on_user_warning(f"The configuration format has changed, altered values:")

      for change in configs_changed:
        self.on_user_warning(f"    {change}")

    if len(channels_changed) > 0:
      self.on_user_warning(f"Application started with {self._nchannel} channels:" )

      for change in channels_changed:
        self.on_user_warning(f"    {change}")

  #-----------------------------------------------------------------------------
  def pack_app( self ):

    layout = {}

    for i in self._manager.state["gui"]["grid_view"].keys():
      layout[i] = self.grid_view[int(i)].save_layout()

    # save the state of the data view layouts
    buf = njm.pack( {
      "state" : self._manager.state,
      "layout" : layout } )

    return buf

  #-----------------------------------------------------------------------------
  def readSettings(self):
    settings = QtCore.QSettings("partis", "partis")
    pos = settings.value("pos", QtCore.QPoint(200, 200))
    size = settings.value("size", QtCore.QSize(400, 400))
    self.resize(size)
    self.move(pos)

    self.restore_time = settings.value("time", None)

    if self.restore_time is not None:
      self.restore_time = float(self.restore_time)

    self.restore_save_file = settings.value( "save_file", None )
    self.restore_buf = settings.value( "state", None )

  #-----------------------------------------------------------------------------
  def writeSettings(self):
      settings = QtCore.QSettings("partis", "partis")
      settings.setValue("pos", self.pos())
      settings.setValue("size", self.size())
      settings.setValue("save_file", self._save_file )
      settings.setValue("time", datetime.timestamp(datetime.now()) )

      # serialize the current state
      buf = self.pack_app()
      settings.setValue( "state", buf )

  #-----------------------------------------------------------------------------
  def on_window_mode( self ):

    if self._is_full_screen:
      self._is_full_screen = False
      self.showNormal()
      # self.setWindowFlags( self.window_flags )
      # self.setWindowState( self.window_state )
    else:
      self._is_full_screen = True
      self.window_flags = self.windowFlags()
      self.window_state = self.windowState()
      # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
      # self.setWindowState( self.window_state ^ QtCore.Qt.WindowFullScreen )
      self.showFullScreen()

  #-----------------------------------------------------------------------------
  def on_user_warning( self, msg ):
    self.dispatch( njm.actions.system.Log( msg ) )

  #-----------------------------------------------------------------------------
  def load_qss_recurse( self, path ):
    path = os.path.normpath( path )

    self._logger.debug( f"Importing stylesheet: {path}" )

    stylesheet_str = None

    with open(path) as fp:
      stylesheet_str = fp.read()

    style_imports = re.finditer(
      r"@import [\"\'](?P<path>[^\"\']+)[\"\']\;",
      stylesheet_str )

    for match in style_imports:
      path = match.group("path")

      imported_str = self.load_qss_recurse( self.resource_path(f'styles/{path}') )

      # include loaded qss file where the @import statement occurs
      stylesheet_str = stylesheet_str.replace( match.group(0), imported_str, 1 )


    return stylesheet_str

  #-----------------------------------------------------------------------------
  def load_qss( self ):
    stylesheet_str = self.load_qss_recurse( self.resource_path('styles/main.qss') )

    return stylesheet_str

  #-----------------------------------------------------------------------------
  def qss_process( self,
    stylesheet_str,
    variables = None,
    px_per_em = None,
    px_per_ex = None,
    px_per_pt = None,
    resource_mode = 'rcc' ):
    """
    Parameters
    ----------
    stylesheet_str : str
      Stylesheet to replace urls
    resource_mode : str
      One of {'rcc', 'file'}:
        rcc: reference to compiled resource file
        file: resolved path to installed resource directory
    """
    assert resource_mode in [ 'rcc', 'file' ]

    url_pattern = r"url\(\s*(?P<path>[^\)]+)\s*\)"
    px_pattern = r"(?P<start>[\:\s])(?P<length>\d+(\.\d+)?)(?P<unit>em|ex|pt)"

    #...........................................................................
    def _replace_rcc(match):
        _path = match.group("path")

        r_path = f":/{_path}"

        return f"url({r_path})"

    #...........................................................................
    def _replace_file(match):
        _path = match.group("path")

        r_path = self.resource_path(
          path = _path )

        r_path = r_path.replace("\\", "/")

        return f"url({r_path})"

    #...........................................................................
    def _replace_px(match):
      unit = match.group("unit")
      length = float(match.group("length"))

      px_per_unit = {
        'pt' : px_per_pt,
        'em' : px_per_em,
        'ex' : px_per_ex }[unit]

      if px_per_unit is None:
        return match.group(0)

      if length == 0.0:
        return f"0px"

      _length = max(
        # NOTE: ensure non-zero length is at least one pixel
        1,
        round( length * px_per_unit ) )

      return f"{_length}px"

    if resource_mode == 'file':
      stylesheet_str = re.sub(
        url_pattern,
        _replace_file,
        stylesheet_str )

    else:
      stylesheet_str = re.sub(
        url_pattern,
        _replace_rcc,
        stylesheet_str )

    if (
      px_per_em is not None
      or px_per_ex is not None
      or px_per_pt is not None ):

      stylesheet_str = re.sub(
        px_pattern,
        _replace_px,
        stylesheet_str )

    return stylesheet_str

  #-----------------------------------------------------------------------------
  def set_theme( self, theme ):

    if self._theme is not None:
      # cleanup previous theme
      if self._theme_rcc is not None:
        QtCore.QResource.unregisterResource( self._theme_rcc )

    self._theme = theme

    import partis.view.themes

    self._theme_module = getattr( partis.view.themes, theme )


    self._resource_dir = os.path.join(
      os.path.dirname(os.path.abspath(__file__)), "themes", self._theme  )

    self._theme_rcc = self.resource_path( '_res.rcc' )

    if not QtCore.QResource.registerResource( self._theme_rcc ):
      raise ImportError(f"Resource file could not be loaded for theme `{theme}`: {self._theme_rcc}")


    fonts_path = self.resource_path( 'fonts', check_exists = False )

    if os.path.exists( fonts_path ):
      fonts = os.listdir(fonts_path)
      rec = re.compile( "^.*\.ttf$" )

      for font in fonts:
        if rec.match( font ):
          path = os.path.join( fonts_path, font )

          self._logger.debug( f"Loading font: {path}" )

          try:
            QtGui.QFontDatabase.addApplicationFont( path )
          except:
            pass

      # self._manager._app.setFont(newFont)


    stylesheet_str = self.load_qss( )


    stylesheet_str = self.qss_process(
      stylesheet_str,
      resource_mode = 'rcc',
      px_per_em = self._px_per_em,
      px_per_ex = self._px_per_ex,
      px_per_pt = None )

    # self._logger.debug(stylesheet_str)

    self.stylesheet = stylesheet_str

    self._manager._app.setStyleSheet( self.stylesheet )

    self.setWindowIcon( QtGui.QIcon(self.resource_path("images/icons/app_icon.png")) )


  #-----------------------------------------------------------------------------
  def resource_path( self,
    path,
    check_exists = True,
    as_url = False ):
    """Converts generic paths to local platform-dependent file path

    Parameters
    ----------
    path : str
      relative path in the theme-specific resource directory
      in forward-slash format
    check_exists : bool
      Raise exception if the file does not exist
    as_url : bool
      Format path as a resource URL
    """

    parts = [ self._resource_dir, ] + path.split("/")
    full_path = os.path.join( *parts )

    if check_exists and not os.path.exists( full_path ):
      raise ValueError(f"Path `{str(full_path)}` not found in the resource directory.")

    if as_url:
      full_path = QtCore.QUrl.fromLocalFile( full_path ).url()

    return full_path

  #-----------------------------------------------------------------------------
  @property
  def theme_module( self ):
    return self._theme_module

  #-----------------------------------------------------------------------------
  async def test_project( self ):
    self._manager.test( self.project )

  #-----------------------------------------------------------------------------
  def show_exception( self, title, exc ):

    dialog = LogDialog(
      manager = self )

    dialog.setWindowTitle( title )

    dialog.log_hint( ModelHint(
      msg = title,
      level = 'error',
      hints = exc ) )

    dialog.exec()

    dialog = None
