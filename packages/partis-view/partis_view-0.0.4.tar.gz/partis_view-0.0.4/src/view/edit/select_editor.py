# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import logging
log = logging.getLogger( __name__ )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import (
  blocked )

from partis.schema import (
  is_mapping )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SelectEditor( QtWidgets.QTreeWidget ):
  double_clicked = QtCore.Signal()

  def __init__(self,
    manager,
    editors,
    default = None ):

    super().__init__()

    self._manager = manager
    self._editors = editors

    self.setGeometry(QtCore.QRect(10, 10, 311, 321))
    self.setObjectName('select_editor')
    self.setSelectionMode( QtWidgets.QAbstractItemView.SingleSelection )
    self.resize(350, 400)

    # set context menu policy
    self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
    self.customContextMenuRequested.connect( self.on_context_menu )
    self.itemDoubleClicked.connect( self.on_double_clicked )

    self.setHeaderHidden(True)

    self._items = dict()
    self._flat_items = dict()

    self.build(
      parent = self,
      editors = self._editors,
      items = self._items,
      path = list(),
      flat_items = self._flat_items )

    if default is None:
      items = self._items

      default = list()

      while isinstance( items, dict ):
        k = next(iter(items.keys()))
        default.append(k)
        items = items[k]

    item = self._items

    for k in default:
      item = item[k]

    self.setCurrentItem(item)

    self.show()
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def build( self, parent, editors, items, path, flat_items ):
    # options is a two level tree.
    # first level is overall type.
    for k, v in editors.items():
      _path = path + [ k, ]

      tree_item = QtWidgets.QTreeWidgetItem( parent )
      tree_item.setText(0, k)
      tree_item.setExpanded(1)

      if isinstance( v, dict ):
        items[k] = dict()

        self.build(
          parent = tree_item,
          editors = v,
          items = items[k],
          path = _path,
          flat_items = flat_items )

      else:
        flat_items[ ".".join(_path) ] = tree_item
        items[k] = tree_item

        tree_item._editor = v


  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def guess_editor( self, filename ):
    guesses = list()

    for k, v in self._flat_items.items():
      guesses.append( (k, v._editor.guess(filename) ) )

    guesses = sorted( guesses, key = lambda obj: obj[1] )

    k, v = guesses[-1]

    self.setCurrentItem(self._flat_items[k])

    return self._flat_items[k]._editor

  #-----------------------------------------------------------------------------
  def on_context_menu(self, point):
    item = self.itemAt( point )

    if item is not None:
      item.setSelected( True )
      item.on_context_menu( self.mapToGlobal(point) )

  #-----------------------------------------------------------------------------
  def on_double_clicked( self, item, col ):

    self.double_clicked.emit()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SelectEditorDialog( QtWidgets.QDialog ):
  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    title,
    editors ):
    super().__init__()

    self._manager = manager

    self.setWindowTitle(title)
    self.setWindowIcon( QtGui.QIcon(manager.resource_path("images/icons/app_icon.png")) )

    self.setStyleSheet( manager.stylesheet )

    self.layout = QtWidgets.QGridLayout()
    self.setLayout(self.layout)

    self._readonly = QtWidgets.QCheckBox( "Open as Read-Only", self )

    self.add_btn = QtWidgets.QPushButton("Add")
    self.add_btn.clicked.connect(self.add)

    self.cancel_btn = QtWidgets.QPushButton("Cancel")
    self.cancel_btn.clicked.connect(self.reject)

    self.select_editor = SelectEditor(
      manager = self._manager,
      editors = editors )

    self.select_editor.double_clicked.connect( self.add )

    self.layout.addWidget(
      self._readonly,
      row = 0,
      column = 0,
      rowSpan = 1,
      columnSpan = 2 )

    self.layout.addWidget(
      self.select_editor,
      row = 1,
      column = 0,
      rowSpan = 1,
      columnSpan = 2 )

    self.layout.addWidget( self.add_btn, 2, 0 )
    self.layout.addWidget( self.cancel_btn, 2, 1 )

    self.selected = None
    self.readonly = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def guess_editor( self, filename ):
    editor = self.select_editor.guess_editor( filename )

    if editor:
      with blocked( self._readonly ):
        self._readonly.setChecked( editor.default_readonly )

    return editor

  #-----------------------------------------------------------------------------
  def add(self):
    selected = self.select_editor.selectedItems()

    if len(selected) > 0 and hasattr(selected[0], "_editor"):
      self.selected = selected[0]._editor
      self.readonly = self._readonly.isChecked()

      self.accept()
