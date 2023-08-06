# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PySide2 import QtCore, QtGui, QtWidgets


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class VariableTreeItem ( QtWidgets.QTreeWidgetItem, QtCore.QObject ):
#
#   clicked = QtCore.Signal(int)
#
#   #-----------------------------------------------------------------------------
#   def __init__( self, parent ):
#     QtWidgets.QTreeWidgetItem.__init__(self, parent)
#     QtCore.QObject.__init__(self)
#
#
#     self._tree = parent._tree
#     self._parent = parent
#
#     self.setExpanded(1)
#     # self.setBackground(0, QtGui.QBrush(QtGui.QColor(117, 88, 69)))
#
#   #-----------------------------------------------------------------------------
#   def on_clicked( self, col ):
#     self.clicked.emit( col )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeItemObject( QtCore.QObject ):
  clicked = QtCore.Signal(int)
  double_clicked = QtCore.Signal(int)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VariableTreeItem ( QtWidgets.QTreeWidgetItem ):

  #-----------------------------------------------------------------------------
  def __init__( self, parent ):
    # QtWidgets.QTreeWidgetItem.__init__(self, parent)
    # QtCore.QObject.__init__(self)
    super().__init__( parent )

    self._tree = parent._tree
    self._parent = parent
    self._object = TreeItemObject()

    self.setExpanded(False)
    # self.setBackground(0, QtGui.QBrush(QtGui.QColor(117, 88, 69)))

  #-----------------------------------------------------------------------------
  @property
  def clicked( self ):
    return self._object.clicked

  #-----------------------------------------------------------------------------
  @property
  def double_clicked( self ):
    return self._object.double_clicked

  #-----------------------------------------------------------------------------
  def on_clicked( self, col ):
    self.clicked.emit( col )

  #-----------------------------------------------------------------------------
  def on_double_clicked( self, col ):
    self.double_clicked.emit( col )
