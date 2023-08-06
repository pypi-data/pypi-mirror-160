"""Usage of `setup.py` is deprecated, and is supplied only for legacy installation.
"""
import sys
import os
import os.path as osp
import importlib
import logging
import argparse
import subprocess
import tempfile
from argparse import RawTextHelpFormatter
logger = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def egg_info( args ):

  logger.warning(
    "running legacy 'setup.py egg_info'" )

  dir = osp.join( args.egg_base, EGG_INFO_NAME )

  if not osp.exists( dir ):
    os.mkdir( dir )

  with open( osp.join( dir, 'PKG-INFO' ), 'wb' ) as fp:
    fp.write( PKG_INFO )

  with open( osp.join( dir, 'setup_requires.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'requires.txt' ), 'wb' ) as fp:
    fp.write( REQUIRES )

  with open( osp.join( dir, 'SOURCES.txt' ), 'wb' ) as fp:
    fp.write( SOURCES )

  with open( osp.join( dir, 'top_level.txt' ), 'wb' ) as fp:
    fp.write( TOP_LEVEL )

  with open( osp.join( dir, 'entry_points.txt' ), 'wb' ) as fp:
    fp.write( ENTRY_POINTS )

  with open( osp.join( dir, 'dependency_links.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'not-zip-safe' ), 'wb' ) as fp:
    fp.write( b'' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_wheel( args ):

  logger.warning(
    "running legacy 'setup.py bdist_wheel'" )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  backend.build_wheel(
    wheel_directory = args.dist_dir or args.bdist_dir or '.' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install( args ):

  logger.warning(
    "running legacy 'setup.py install'" )

  reqs = [ f"{r}" for r in build_requires ]

  subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    *reqs ] )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  with tempfile.TemporaryDirectory() as tmpdir:
    wheel_name = backend.build_wheel(
      wheel_directory = tmpdir )

    subprocess.check_call([
      sys.executable,
      '-m',
      'pip',
      'install',
      osp.join(tmpdir, wheel_name) ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dummy( args ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  logging.basicConfig(
    level = logging.INFO,
    format = "{name}:{levelname}: {message}",
    style = "{" )


  logger.warning(
    "'setup.py' is deprecated, limited support for legacy installs. Upgrade pip." )

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  subparsers = parser.add_subparsers()

  #.............................................................................
  egg_info_parser = subparsers.add_parser( 'egg_info' )

  egg_info_parser.set_defaults( func = egg_info )

  egg_info_parser.add_argument( "-e", "--egg-base",
    type = str,
    default = '.' )

  #.............................................................................
  bdist_wheel_parser = subparsers.add_parser( 'bdist_wheel' )

  bdist_wheel_parser.set_defaults( func = bdist_wheel )

  bdist_wheel_parser.add_argument( "-b", "--bdist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "-d", "--dist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "--python-tag",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--plat-name",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--py-limited-api",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--build-number",
    type = str,
    default = None )

  #.............................................................................
  install_parser = subparsers.add_parser( 'install' )

  install_parser.set_defaults( func = install )

  install_parser.add_argument( "--record",
    type = str,
    default = None )

  install_parser.add_argument( "--install-headers",
    type = str,
    default = None )

  install_parser.add_argument( "--compile",
    action='store_true' )

  install_parser.add_argument( "--single-version-externally-managed",
    action='store_true' )

  #.............................................................................
  clean_parser = subparsers.add_parser( 'clean' )

  clean_parser.set_defaults( func = dummy )

  clean_parser.add_argument( "-a", "--all",
    action='store_true' )

  args = parser.parse_args( )

  args.func( args )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE: these are templated literal values substituded by the backend when
# building the source distribution

build_backend = 'partis.pyproj.backend'
backend_path = []
build_requires = ['partis-pyproj==0.0.3', 'PySide2<5.16,>=5.15; python_version >= "3.8"', 'wheel', 'PySide2<5.15,>=5.14; python_version < "3.8"', 'lxml>=4.2.5']

EGG_INFO_NAME = 'partis-view.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-view\nVersion: 0.0.3\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Graphical interface for viewing and editing workflow files\nLicense-File: LICENSE.txt\nClassifier: Development Status :: 4 - Beta\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Intended Audience :: Science/Research\nClassifier: Programming Language :: Python\nClassifier: Operating System :: POSIX :: Linux\nClassifier: Topic :: Scientific/Engineering\nClassifier: Programming Language :: Python :: 3\nClassifier: Topic :: System :: Clustering\nProvides-Extra: doc\nRequires-Dist: PySide2<5.15,>=5.14; python_version < "3.8"\nRequires-Dist: partis-schema==0.0.3\nRequires-Dist: partis-pyproj==0.0.3\nRequires-Dist: PySide2<5.16,>=5.15; python_version >= "3.8"\nRequires-Dist: wheel\nRequires-Dist: scipy>=1.3.1\nRequires-Dist: partis-utils[asy,theme]==0.0.3\nRequires-Dist: lxml>=4.2.5\nRequires-Dist: partis-utils[sphinx]==0.0.3; extra == "doc"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.view`` package is a graphical interface for viewing and editing workflow files.\n\nhttps://nanohmics.bitbucket.io/doc/partis/view'

REQUIRES = b'PySide2<5.15,>=5.14; python_version < "3.8"\npartis-schema==0.0.3\npartis-pyproj==0.0.3\nPySide2<5.16,>=5.15; python_version >= "3.8"\nwheel\nscipy>=1.3.1\npartis-utils[asy,theme]==0.0.3\nlxml>=4.2.5\npartis-utils[sphinx]==0.0.3; extra == "doc"'

SOURCES = b'partis_view-0.0.3/src/view/__init__.py\npartis_view-0.0.3/src/view/dialog/__init__.py\npartis_view-0.0.3/src/view/dialog/hint.py\npartis_view-0.0.3/src/view/dialog/log.py\npartis_view-0.0.3/src/view/dialog/progress.py\npartis_view-0.0.3/src/view/__main__.py\npartis_view-0.0.3/src/view/main_window.py\npartis_view-0.0.3/src/view/themes/__init__.py\npartis_view-0.0.3/src/view/themes/light/__init__.py\npartis_view-0.0.3/src/view/themes/light/pygments_style.py\npartis_view-0.0.3/src/view/themes/light/images/icons/vsplit.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/new.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/vhsplit.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/settings.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/forward.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/save.svg.2019_07_22_11_53_11.0.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/remove_hover.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/move_down.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/hsplit.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/move_up.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/script_active.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/base.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/down_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/save.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/load.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/back.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/script.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/config.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/left_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/edit.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/restore.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/remove_pressed.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/right_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/up_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/add.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/app_icon.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/edit_2.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/pancake.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/app_icon.png\npartis_view-0.0.3/src/view/themes/light/images/icons/disk.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/remove.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/connect.svg\npartis_view-0.0.3/src/view/themes/light/images/icons/saveAs.svg\npartis_view-0.0.3/src/view/themes/light/images/tree/branch-skip.svg\npartis_view-0.0.3/src/view/themes/light/images/tree/branch-end.svg\npartis_view-0.0.3/src/view/themes/light/images/tree/branch-more.svg\npartis_view-0.0.3/src/view/themes/light/images/tree/branch-closed.svg\npartis_view-0.0.3/src/view/themes/light/images/tree/branch-open.svg\npartis_view-0.0.3/src/view/themes/light/images/base/undock-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/right_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/radio_checked-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/down_arrow-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/radio_checked_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/transparent.svg\npartis_view-0.0.3/src/view/themes/light/images/base/up_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/branch_closed-on.svg\npartis_view-0.0.3/src/view/themes/light/images/base/down_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_checked_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/spinup_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/left_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/stylesheet-vline.svg\npartis_view-0.0.3/src/view/themes/light/images/base/stylesheet-branch-more.svg\npartis_view-0.0.3/src/view/themes/light/images/base/left_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_checked-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/branch_open-on.svg\npartis_view-0.0.3/src/view/themes/light/images/base/radio_unchecked_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/vsepartoolbars.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_unchecked_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/hmovetoolbar.svg\npartis_view-0.0.3/src/view/themes/light/images/base/stylesheet-branch-end-open.svg\npartis_view-0.0.3/src/view/themes/light/images/base/hsepartoolbar.svg\npartis_view-0.0.3/src/view/themes/light/images/base/stylesheet-branch-end.svg\npartis_view-0.0.3/src/view/themes/light/images/base/right_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_indeterminate_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/radio_unchecked-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/vmovetoolbar.svg\npartis_view-0.0.3/src/view/themes/light/images/base/up_arrow.svg\npartis_view-0.0.3/src/view/themes/light/images/base/close-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/stylesheet-branch-end-closed.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_unchecked-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/down_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/light/images/base/up_arrow-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/sizegrip.svg\npartis_view-0.0.3/src/view/themes/light/images/base/radio_checked.svg\npartis_view-0.0.3/src/view/themes/light/images/base/close-pressed.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_indeterminate-hover.svg\npartis_view-0.0.3/src/view/themes/light/images/base/close.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_indeterminate.svg\npartis_view-0.0.3/src/view/themes/light/images/base/branch_closed.svg\npartis_view-0.0.3/src/view/themes/light/images/base/branch_open.svg\npartis_view-0.0.3/src/view/themes/light/images/base/undock.svg\npartis_view-0.0.3/src/view/themes/light/images/base/checkbox_checked.svg\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Regular.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-LightItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Thin.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-BoldItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Italic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-MediumItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-BoldItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-BlackItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-LightItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Medium.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Bold.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Italic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-ThinItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/LICENSE.txt\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Thin.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Black.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Light.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-MediumItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Light.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/RobotoMono-Regular.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Medium.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-ThinItalic.ttf\npartis_view-0.0.3/src/view/themes/light/fonts/Roboto-Bold.ttf\npartis_view-0.0.3/src/view/themes/light/styles/main.qss\npartis_view-0.0.3/src/view/themes/light/styles/base.qss\npartis_view-0.0.3/src/view/themes/light/styles/config_tree.qss\npartis_view-0.0.3/src/view/themes/dark/__init__.py\npartis_view-0.0.3/src/view/themes/dark/pygments_style.py\npartis_view-0.0.3/src/view/themes/dark/images/icons/vsplit.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/new.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/script.svg.2021_05_20_09_51_07.0.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/vhsplit.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/settings.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/forward.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/save.svg.2019_07_22_11_53_11.0.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/remove_hover.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/move_down.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/hsplit.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/move_up.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/script_active.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/base.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/down_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/save.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/load.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/back.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/script.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/config.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/left_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/edit.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/restore.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/remove_pressed.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/right_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/up_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/add.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/app_icon.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/edit_2.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/pancake.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/app_icon.png\npartis_view-0.0.3/src/view/themes/dark/images/icons/remove.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/connect.svg\npartis_view-0.0.3/src/view/themes/dark/images/icons/saveAs.svg\npartis_view-0.0.3/src/view/themes/dark/images/test/no_data.png\npartis_view-0.0.3/src/view/themes/dark/images/test/no_data_pattern.png\npartis_view-0.0.3/src/view/themes/dark/images/test/no_data.svg\npartis_view-0.0.3/src/view/themes/dark/images/test/no_data_pattern.svg\npartis_view-0.0.3/src/view/themes/dark/images/test/pattern.png\npartis_view-0.0.3/src/view/themes/dark/images/tree/branch-skip.svg\npartis_view-0.0.3/src/view/themes/dark/images/tree/stylesheet-branch-more.png\npartis_view-0.0.3/src/view/themes/dark/images/tree/branch-end.svg\npartis_view-0.0.3/src/view/themes/dark/images/tree/branch-more.svg\npartis_view-0.0.3/src/view/themes/dark/images/tree/branch-closed.svg\npartis_view-0.0.3/src/view/themes/dark/images/tree/branch-open.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/undock-hover.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/right_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/down_arrow-hover.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/readme.md\npartis_view-0.0.3/src/view/themes/dark/images/base/radio_checked_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/transparent.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/up_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/branch_closed-on.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/down_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_checked_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/spinup_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/left_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/stylesheet-vline.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/stylesheet-branch-more.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/left_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/branch_open-on.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/radio_unchecked_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/vsepartoolbars.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_unchecked_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/hmovetoolbar.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/stylesheet-branch-end-open.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/hsepartoolbar.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/stylesheet-branch-end.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/right_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_unchecked.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_indeterminate_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/vmovetoolbar.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_unchecked_active.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/up_arrow.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/close-hover.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/stylesheet-branch-end-closed.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/down_arrow_disabled.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/up_arrow-hover.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/sizegrip.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/radio_unchecked.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/radio_checked.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/close-pressed.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/close.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_indeterminate.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/branch_closed.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/branch_open.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/undock.svg\npartis_view-0.0.3/src/view/themes/dark/images/base/checkbox_checked.svg\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Regular.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-LightItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Thin.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-BoldItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Italic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-MediumItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-BoldItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-BlackItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-LightItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Medium.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Bold.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Italic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-ThinItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/LICENSE.txt\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Thin.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Black.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Light.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-MediumItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Light.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/RobotoMono-Regular.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Medium.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-ThinItalic.ttf\npartis_view-0.0.3/src/view/themes/dark/fonts/Roboto-Bold.ttf\npartis_view-0.0.3/src/view/themes/dark/styles/main.qss\npartis_view-0.0.3/src/view/themes/dark/styles/base.qss\npartis_view-0.0.3/src/view/themes/dark/styles/config_tree.qss\npartis_view-0.0.3/src/view/edit/variables/multi_str_w.py\npartis_view-0.0.3/src/view/edit/variables/__init__.py\npartis_view-0.0.3/src/view/edit/variables/record_w.py\npartis_view-0.0.3/src/view/edit/variables/gen_str_w.py\npartis_view-0.0.3/src/view/edit/variables/select_w.py\npartis_view-0.0.3/src/view/edit/variables/int_w.py\npartis_view-0.0.3/src/view/edit/variables/array_w.py\npartis_view-0.0.3/src/view/edit/variables/filepath_w.py\npartis_view-0.0.3/src/view/edit/variables/base.py\npartis_view-0.0.3/src/view/edit/variables/float_spline_2d.py\npartis_view-0.0.3/src/view/edit/variables/float_w.py\npartis_view-0.0.3/src/view/edit/variables/bool_w.py\npartis_view-0.0.3/src/view/edit/__init__.py\npartis_view-0.0.3/src/view/edit/workdir.py\npartis_view-0.0.3/src/view/edit/select_editor.py\npartis_view-0.0.3/src/view/edit/editor_map.py\npartis_view-0.0.3/src/view/edit/project.py\npartis_view-0.0.3/src/view/edit/file_editor.py\npartis_view-0.0.3/src/view/edit/plugin.py\npartis_view-0.0.3/src/view/edit/text/__init__.py\npartis_view-0.0.3/src/view/edit/text/plaintext.py\npartis_view-0.0.3/src/view/edit/text/code.py\npartis_view-0.0.3/src/view/edit/var_tree/__init__.py\npartis_view-0.0.3/src/view/edit/var_tree/var_tree.py\npartis_view-0.0.3/src/view/edit/var_tree/var_tree_item.py\npartis_view-0.0.3/src/view/edit/schema_editor.py\npartis_view-0.0.3/src/view/base/crumbs.py\npartis_view-0.0.3/src/view/base/__init__.py\npartis_view-0.0.3/src/view/base/base.py\npartis_view-0.0.3/src/view/base/widget_stack.py\npartis_view-0.0.3/src/view/manager.py\npartis_view-0.0.3/src/view/schema/tree_edit_deligate.py\npartis_view-0.0.3/src/view/schema/__init__.py\npartis_view-0.0.3/src/view/schema/tree_edit_w.py\npartis_view-0.0.3/src/view/schema/edit_w.py\npartis_view-0.0.3/src/view/schema/name_w.py\npartis_view-0.0.3/src/view/schema/int_w.py\npartis_view-0.0.3/src/view/schema/pass_w.py\npartis_view-0.0.3/src/view/schema/str_w.py\npartis_view-0.0.3/src/view/schema/hint_w.py\npartis_view-0.0.3/src/view/schema/union_w.py\npartis_view-0.0.3/src/view/schema/map_w.py\npartis_view-0.0.3/src/view/schema/tree_node_map.py\npartis_view-0.0.3/src/view/schema/type_combo_w.py\npartis_view-0.0.3/src/view/schema/optional_w.py\npartis_view-0.0.3/src/view/schema/struct_w.py\npartis_view-0.0.3/src/view/schema/evaluated_w.py\npartis_view-0.0.3/src/view/schema/float_w.py\npartis_view-0.0.3/src/view/schema/bool_w.py\npartis_view-0.0.3/src/view/schema/tree_edit_node.py\npartis_view-0.0.3/src/view/schema/list_w.py\npartis_view-0.0.3/src/view/highlight/__init__.py\npartis_view-0.0.3/src/view/highlight/pygments.py\npartis_view-0.0.3/doc/conf.py\npartis_view-0.0.3/doc/__init__.py\npartis_view-0.0.3/doc/index.rst\npartis_view-0.0.3/doc/src/partis.view.__main__.rst\npartis_view-0.0.3/doc/__main__.py\npartis_view-0.0.3/test/conftest.py\npartis_view-0.0.3/test/900_view/conftest.py\npartis_view-0.0.3/test/900_view/__init__.py\npartis_view-0.0.3/test/900_view/test_901_app.py\npartis_view-0.0.3/pkgaux/build_qrc.py\npartis_view-0.0.3/pkgaux/__init__.py\npartis_view-0.0.3/pyproject.toml\npartis_view-0.0.3/LICENSE.txt\npartis_view-0.0.3/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b'[console_scripts]\npartis-view = partis.view.__main__:main\n\n'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
