# -*- coding: UTF-8 -*-

import os

try:
  from importlib.metadata import distributions

except ImportError:
  from importlib_metadata import distributions

from partis.utils import getLogger
log = getLogger(__name__)

from partis.utils.plugin import (
  plugin_manager )

from .text import (
  PlainTextEditor )

from .schema_editor import (
  SchemaTreeFileEditor )

from partis.schema.plugin import (
  SchemaPluginGroup )

from .plugin import (
  EditorPluginGroup,
  SchemaEditNodePlugin )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditorMap:

  #-----------------------------------------------------------------------------
  @property
  def editors( self ):

    editors = {
      "Plain Text" : PlainTextEditor,
      "YAML" : SchemaTreeFileEditor }

    editor_schemas = set()

    for plugin in plugin_manager.plugins( EditorPluginGroup ):

      if plugin.label:
        group_editors = editors.setdefault( plugin.label, dict() )
      else:
        # root level group
        group_editors = editors

      for k, v in plugin.editors.items():

        group_editors[k] = v

        editor_schemas.add( v.default_schema.schema )

    for plugin in plugin_manager.plugins( SchemaPluginGroup ):

      group_editors = dict()

      for k, v in plugin.schemas.items():
        if v not in editor_schemas:
          group_editors[k] = SchemaTreeFileEditor.specialize_schema(v)

      if group_editors:
        editors[plugin.label] = group_editors

    return editors

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
editor_map = EditorMap()
