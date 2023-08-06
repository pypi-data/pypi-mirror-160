# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from .log import (
  LogWidgetHandler,
  LogWidget )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProgressBar( QtWidgets.QProgressBar ):
  #-----------------------------------------------------------------------------
  def __init__(self, *args, **kwargs ):
    super().__init__( *args, **kwargs )

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProgressDialog ( QtWidgets.QDialog ):
  """
  """
  #-----------------------------------------------------------------------------
  def __init__( self, manager, with_log = False ):
    super( ).__init__( manager )

    # self.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.Dialog )
    self.setWindowIcon( QtGui.QIcon(manager.resource_path("images/icons/app_icon.png")) )
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )
    self.setStyleSheet( manager.stylesheet )

    self.setWindowTitle("")

    self._manager = manager
    self._with_log = with_log

    self._layout = QtWidgets.QVBoxLayout()

    self.setLayout( self._layout )

    self._pbar = ProgressBar()
    self._layout.addWidget( self._pbar )
    self._pbar.setAlignment( QtCore.Qt.AlignHCenter )


    self._label = QtWidgets.QLabel()
    self._layout.addWidget( self._label )
    self._label.setAlignment( QtCore.Qt.AlignHCenter )

    self._log = None
    self._log_handler = None

    if self._with_log:
      self._log = LogWidget( self._manager )
      self._layout.addWidget( self._log )

      self._log_handler = LogWidgetHandler(
        widget = self._log )

    # screen = QtGui.QGuiApplication.primaryScreen()
    # screenGeometry = screen.geometry()
    # height = screenGeometry.height()
    # width = screenGeometry.width()
    #
    # self.resize( int( width / 2.0 ), int( height / 2.0 ) )


  #-----------------------------------------------------------------------------
  @property
  def log_handler( self ):
    return self._log_handler

  #-----------------------------------------------------------------------------
  def sizeHint(self):
    if self._with_log:
      return QtCore.QSize( 600, 400 )
    else:
      return QtCore.QSize( 400, 100 )

  #-----------------------------------------------------------------------------
  def set_title( self, value ):
    self.setWindowTitle(value)

  #-----------------------------------------------------------------------------
  def set_status( self, value ):
    self._label.setText( value )

  #-----------------------------------------------------------------------------
  def reset( self ):
    self._pbar.reset()

  #-----------------------------------------------------------------------------
  def set_range( self, min, max ):
    self._pbar.setRange( min, max )

  #-----------------------------------------------------------------------------
  def set_value( self, value ):
    self._pbar.setValue( value )
