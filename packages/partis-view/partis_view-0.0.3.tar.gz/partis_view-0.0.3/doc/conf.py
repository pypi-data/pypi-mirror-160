# -*- coding: utf-8 -*-

from partis.utils.sphinx import basic_conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# configuration
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

globals().update( basic_conf(
  package = 'partis-view',
  copyright_year = '2022' ) )


intersphinx_mapping['partis.pyproj'] = (
  "https://nanohmics.bitbucket.io/doc/partis/pyproj",
  None )

intersphinx_mapping['partis.utils'] = (
  "https://nanohmics.bitbucket.io/doc/partis/utils",
  None )

intersphinx_mapping['partis.schema'] = (
  "https://nanohmics.bitbucket.io/doc/partis/schema",
  None )

intersphinx_mapping['partis.nwl'] = (
  "https://nanohmics.bitbucket.io/doc/partis/pyproj",
  None )
