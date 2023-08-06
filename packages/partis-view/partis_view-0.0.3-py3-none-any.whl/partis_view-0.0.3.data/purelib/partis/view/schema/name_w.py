# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets


from partis.schema_meta.base import (
  name_re,
  name_cre )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RenameDialog ( QtWidgets.QDialog ):
  """
  """
  #-----------------------------------------------------------------------------
  def __init__( self, manager, name ):
    super( ).__init__( manager )

    # self.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.Dialog )
    self.setWindowIcon( QtGui.QIcon(manager.resource_path("images/icons/app_icon.png")) )
    self.setStyleSheet( manager.stylesheet )

    self.setWindowTitle("Rename")

    self._manager = manager
    self._name = name

    self._layout = QtWidgets.QVBoxLayout()

    self.setLayout( self._layout )

    self._line =  QtWidgets.QLineEdit()
    self._line.setPlaceholderText( self._name )

    self._line.setValidator( QtGui.QRegExpValidator(
      name_re ) )

    self._layout.addWidget( QtWidgets.QLabel("New Name:") )
    self._layout.addWidget( self._line )

    buttonBox = QtWidgets.QDialogButtonBox(
      QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel )

    self._layout.addWidget(buttonBox)
    buttonBox.accepted.connect( self.accept )
    buttonBox.rejected.connect( self.reject )
    self.accepted.connect( self.on_accept )

    # screen = QtGui.QGuiApplication.primaryScreen()
    # screenGeometry = screen.geometry()
    # height = screenGeometry.height()
    # width = screenGeometry.width()
    #
    # self.resize( int( width / 2.0 ), int( height / 2.0 ) )

  #-----------------------------------------------------------------------------
  def on_accept( self ):
    name = str( self._line.text() )

    if name_cre.fullmatch(name) is not None:

      self._name = name

  #-----------------------------------------------------------------------------
  @property
  def name( self ):
    return self._name
