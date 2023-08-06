# -*- coding: UTF-8 -*-

from partis.utils import getLogger
log = getLogger(__name__)

from partis.utils.plugin import (
  Plugin,
  PluginError )

from partis.schema import (
  is_string,
  is_schema )

from .file_editor import (
  FileEditor,
  TextFileEditor )

from .schema_editor import (
  SchemaFileEditor,
  SchemaTreeFileEditor,
  SchemaStructTreeFileEditor )

from partis.view.schema import (
  TreeEditNode,
  TreeEditNodeMap )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditorPluginError( PluginError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditorPluginGroup( Plugin ):
  """Group of editors to load as a plugin

  Parameters
  ----------
  editors : dict[str, FileEditor]
    Dictionary of loaded editors. Keys are the labels for each editor in the
    group.
  label : str | None
    User-friendly label for the group of editors loaded by this plugin
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    editors,
    label = None ):

    if label is None:
      label = ''

    for k, v in editors.items():
      if not issubclass(v, FileEditor):
        raise EditorPluginError(
          f'Value must be subclass of FileEditor: {type(v)}' )

      if not is_string(k):
        raise EditorPluginError(
          f'Key must be a string: {type(k)}' )

    self._p_label = str(label)
    self._p_editors = dict(editors)

  #-----------------------------------------------------------------------------
  @property
  def label(self):
    return self._p_label

  #-----------------------------------------------------------------------------
  @property
  def editors(self):
    return self._p_editors

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaEditNodePlugin( Plugin ):
  """Group of editors to load as a plugin

  Parameters
  ----------
  editor : SchemaFileEditor
    The editor to use for instances of the given schema
  node_map : dict[ Schema, :class:`partis.view.schema.tree_node_w.TreeEditNode` ]
    Mapping of schemas to tree nodes

  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    editor,
    node_map ):


    if not (
      issubclass( editor, SchemaTreeFileEditor )
      or issubclass( editor, SchemaStructTreeFileEditor ) ):

      raise EditorPluginError(
        f"'editor' must be subclass of SchemaTreeFileEditor or SchemaStructTreeFileEditor: {v}" )


    for k, v in node_map.items():
      if not is_schema(k):
        raise EditorPluginError(
          f'Key must be a Schema: {type(k)}' )

      if not issubclass( v, TreeEditNode ):
        raise EditorPluginError(
          f"Value must be subclass of TreeEditNode: {v}" )


    self._p_editor = editor

    self._p_node_map = node_map

  #-----------------------------------------------------------------------------
  @property
  def editor(self):
    return self._p_editor

  #-----------------------------------------------------------------------------
  @property
  def node_map(self):
    return self._p_node_map
