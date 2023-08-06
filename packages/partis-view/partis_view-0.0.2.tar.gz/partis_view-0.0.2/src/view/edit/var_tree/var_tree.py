# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import ConfigTree

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VariableTree ( ConfigTree ):
  def __init__(self, manager, ncols = 7, header = False ):
    super().__init__()

    self._manager = manager
    self._state = None
    self._tree = self

    self._columns = ["",] * ncols

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    # self.setStyleSheet( manager.stylesheet )

    self.setAlternatingRowColors(True)

    self.setVerticalScrollMode( QtWidgets.QTreeView.ScrollPerPixel )

    self.setColumnCount(len(self._columns))
    self.setHeaderLabels(self._columns)

    self.setGeometry(QtCore.QRect(10, 10, 311, 321))
    self.setObjectName('treeWidget')
    self.setSelectionMode (QtWidgets.QAbstractItemView.SingleSelection)
    # self.resize(350, 400)
    self.header().setSectionResizeMode( QtWidgets.QHeaderView.ResizeToContents )
    self.header().setSectionsMovable( False )
    # self.resizeColumnToContents( True )
    # self.setSortingEnabled( False )

    if not header:
      self.header().setVisible(False)

    # set context menu policy
    self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
    self.customContextMenuRequested.connect( self.on_context_menu )

    self._items = {}

    self.show()

    self.itemClicked.connect( self.on_item_clicked )
    self.itemDoubleClicked.connect( self.on_item_double_clicked )


  #-----------------------------------------------------------------------------
  def on_context_menu(self, point):

    item = self.itemAt( point )

    if item is not None:
      item.setSelected( True )

      if hasattr( item, 'on_context_menu' ):
        item.on_context_menu( self.mapToGlobal(point) )

  #-----------------------------------------------------------------------------
  def on_item_clicked( self, item, col ):
    item.on_clicked( col )

  #-----------------------------------------------------------------------------
  def on_item_double_clicked( self, item, col ):
    item.on_double_clicked( col )
