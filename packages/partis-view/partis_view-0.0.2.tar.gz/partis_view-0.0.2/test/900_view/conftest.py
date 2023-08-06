

import os
import sys
import shutil
import pytest
import logging
log = logging.getLogger(__name__)

XVFB_AVAIL = False

try:
  # disables gui tests if a virtual display cannot be created
  import pyvirtualdisplay
  XVFB_AVAIL = shutil.which('Xvfb') is not None
except:
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# https://docs.pytest.org/en/6.2.x/reference.html#hook-reference
def pytest_configure( config ):
  """Allow plugins and conftest files to perform initial configuration.
  """

  config.vdisplay = None
  config.addinivalue_line(
    "markers",
    "with_gui: Skip test if partis[gui], virtual display, is not available" )

  if XVFB_AVAIL:
    # Taken from pytest-xvfb
    # Implemented here for more fine-grained control over the virtual display
    # and debugging of related issues at run-time
    # https://github.com/The-Compiler/pytest-xvfb

    width = int(config.getini('vdisplay_width'))
    height = int(config.getini('vdisplay_height'))
    colordepth = int(config.getini('vdisplay_colordepth'))

    log.debug("virtual display starting")

    try:
      config.vdisplay = pyvirtualdisplay.Display(
        backend = 'xvfb',
        size = ( width, height ),
        color_depth = colordepth,
        use_xauth = False,
        extra_args = list() )

      config.vdisplay.start()

    except Exception as e:
      log.exception( f"Failed to start virtual display" )

    if config.vdisplay is not None and not config.vdisplay.is_alive():
      log.error( f"virtual display is not running" )
      log.error( config.vdisplay.stdout or "[no virtual display stdout]")
      log.error( config.vdisplay.stderr or "[no virtual display stderr]")

      config.vdisplay = None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pytest_unconfigure(config):
  """Called before test process is exited.
  """

  log.debug("virtual display stopping")
  vdisplay = getattr( config, 'vdisplay', None )

  if vdisplay is not None:
    if config.vdisplay.is_alive():
      config.vdisplay.stop()
      config.vdisplay = None
    else:
      log.error( f"virtual display was no longer running" )
      log.error( config.vdisplay.stdout or "[no virtual display stdout]" )
      log.error( config.vdisplay.stderr or "[no virtual display stderr]" )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pytest_collection_modifyitems(items):
  for item in items:
    vdisplay = getattr( item.config, 'vdisplay', None )

    if vdisplay is not None and not vdisplay.is_alive():
      log.error( f"virtual display is not alive" )
      vdisplay = None

    if item.get_closest_marker('with_gui'):

      if vdisplay is None:

        with_vdisplay_marker = pytest.mark.skipif(
          True,
          reason = "No virtual display. Make sure Xvfb is installed and available to run test" )

        item.add_marker( with_vdisplay_marker )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def pytest_runtest_setup(item):
  # called for running each test in 'a' directory
  print("setting up", item)
