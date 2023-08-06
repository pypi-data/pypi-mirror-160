# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)



from partis.view.system.config.variables import var_widgets

from partis.view.base import ( Heading1, Heading2, Heading3, HLine )

from .base import VariableWidget
from ..var_tree import VariableTreeItem

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructVarWidget( VariableWidget ):

  changed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    type,
    heading_level = 0,
    tag = 'config',
    tree_parent = None ):

    super( ).__init__()

    self._manager = manager
    self._type = type
    self._tag = tag
    self._tree_parent = tree_parent
    self._tree_item = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    if self._tree_parent is not None:

      self._tree_item = VariableTreeItem(
        manager = self._manager,
        tree = self._tree_parent._tree if isinstance( self._tree_parent, VariableTreeItem ) else self._tree_parent,
        parent = self._tree_parent )

      self._tree_item.setText( 0, self._type.label )
      self._tree_item._tree.setItemWidget( self._tree_item, 4, self )

      if type.info is not None:
        tooltip = "<FONT>" + type.info + "</FONT>"
        self._tree_item.setToolTip( 0, tooltip )

    else:
      self.vlayout = QtWidgets.QVBoxLayout(self)
      self.setLayout(self.vlayout)

      heading_class = heading_levels[ min( len(heading_levels)-1, heading_level) ]
      self.title = heading_class( self._type.label )

      self.vlayout.addWidget(
        self.title,
        alignment = QtCore.Qt.AlignLeft )

    # variable widgets at equal level
    self._var_widgets = {}
    # sub-variable groups
    self._var_groups = {}


    for var, var_type in self._type.vars.items():

      if var_type.tag_any( self._tag ):

        if isinstance( var_type, njm.config.base.DictType ):
          # this is a sub-configuration widget

          widget = StructVarWidget(
            manager,
            var_type,
            heading_level = heading_level + 1,
            tag = self._tag,
            tree_parent = self._tree_item )

          widget.adjustSize()

          widget.changed.connect( self.on_change )

          self._var_groups[var] = widget

          if self._tree_item is None:
            self.vlayout.addWidget( HLine() )
            self.vlayout.addWidget( widget )

        else:
          widget = var_widgets[ var_type.__class__ ](
            manager = manager,
            type = var_type,
            config = self,
            tree_parent = self._tree_item )

          widget.adjustSize()

          widget.changed.connect( self.on_change )

          self._var_widgets[var] = widget

          if self._tree_item is None:
            self.vlayout.addWidget( widget )

    if self._tree_item is None:
      self.vlayout.addStretch( 1 )

    self.adjustSize()

    self._state = None

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  def set_state( self, state ):
    self._state = state

    for var, var_type in self._type.vars.items():

      widget = None

      if var in self._var_groups:

        widget = self._var_groups[var]

        widget.set_state( state[var] )

      elif var in self._var_widgets:

        widget = self._var_widgets[var]

        widget.set_value( state[var] )

      if widget is not None:
        widget.set_enabled( var_type.enabled( state ) )

        widget.set_visible( var_type.exists( state ) )

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )

      for var, var_type in self._type.vars.items():

        widget = None

        if var in self._var_groups:

          widget = self._var_groups[var]

        elif var in self._var_widgets:

          widget = self._var_widgets[var]

        if widget is not None:
          widget.set_enabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #-----------------------------------------------------------------------------
  def get_value ( self ):

    new_config = {}

    for var, var_type in  self._type.vars.items():
      if var in self._var_groups:
        new_config[var] = self._var_groups[var].get_value()
      elif var in self._var_widgets:
        new_config[var] = self._var_widgets[var].get_value()

    new_state = self._state.update( "", njm.base.State("", new_config ) )

    return new_state

  #----------------------------------------------------------------------------#
  def on_change( self, _ ):
    self.changed.emit( self.get_value() )
