import os
import os.path as osp
import re
import subprocess
import sys
import shutil
import stat

# various names by which the rcc command may go by
RCC_ALIASES = [
  'rcc',
  'pyside2-rcc',
  'rcc.exe',
  'pyside2-rcc.exe' ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def find_rcc():


  # first search directly in any PySide installation
  try:
    import PySide2

  except ImportError as e:
    print(e)

  else:
    dir = osp.dirname( PySide2.__file__ )

    # search relative to install directory
    search_paths = [
      '.',
      osp.join( 'Qt', 'libexec', 'rcc' ) ]

    for path in search_paths:
      for name in RCC_ALIASES:
        _rcc = osp.join( dir, path, name )

        if osp.exists( _rcc ) and osp.isfile( _rcc ):
          return _rcc

  # if that failsm attempt regular 'which' type executable search
  # NOTE: build isolation can cause problems with commands installed in a bin
  # that reference packages not available in the build environment
  for name in RCC_ALIASES:
    _rcc = shutil.which( name )

    if _rcc:
      return _rcc


  return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _build_qrc(
  rcc_cmd,
  res_path,
  qrc_path,
  rcc_path,
  rinclude = None,
  rignore = None ):
  """Builds a Qt Resource (qrc) xml file by traversing a directory tree

  Parameters
  ----------
  rcc_cmd : str
    Name of the `rcc` command used to build qrc
  res_path : str
    Path to directory of resource files
  qrc_path : str
    Path to generate .qrc resource file
  rcc_path : str
    Path to generate binary resource file
  rinclude : None | str
    Pattern used to match filenames
  rignore : None | str
    Pattern used to match filenames

  """

  # ensure the command is executable
  # NOTE: running `pip install --no-deps ...` appears to not set executable flag
  # on dependency files ( i.e. rcc from PySide2 )
  # TODO: understand if lack of execute permissions are expected behaviour, and why
  if not os.access( rcc_cmd, os.X_OK ):
    # Attempt to change file permission to executable, may fail if no permission
    os.chmod(
      rcc_cmd,
      os.stat(rcc_cmd).st_mode | stat.S_IXUSR )

  import lxml.etree as ET

  if rinclude is not None:
    rinclude = re.compile( rinclude )

  if rignore is not None:
    rignore = re.compile( rignore )

  rcc_doc = ET.Element(
    "RCC",
    attrib = { "version" : "1.0" } )

  qresource = ET.SubElement(
    rcc_doc,
    "qresource" )

  for root, dirs, files in os.walk( res_path ):
    for file in files:
      if (
        ( rinclude is None or rinclude.match(file) )
        and ( rignore is None or not rignore.match(file) ) ):

        _path = osp.relpath(
          osp.join( root, file ),
          start = res_path )

        file_el = ET.SubElement(
          qresource,
          "file" )

        file_el.text = _path

  rcc_doc_txt = ET.tostring(
    rcc_doc,
    encoding = "utf-8",
    pretty_print = True )


  with open( qrc_path, "wb" ) as f:
    f.write( rcc_doc_txt )

  subprocess.check_call([
    rcc_cmd,
    "--binary",
    '--output', rcc_path,
    qrc_path ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def build_qrc(
  src,
  dst,
  prefix ):

  rcc_cmd = find_rcc()

  if not rcc_cmd:
    raise ValueError(f"rcc command not found")

  _build_qrc(
    rcc_cmd = rcc_cmd,
    res_path = src,
    qrc_path = osp.join( dst, f"{prefix}.qrc" ),
    rcc_path = osp.join( dst, f"{prefix}.rcc" ),
    rignore = r"^\w+\.(py|qrc|rcc)$" )
