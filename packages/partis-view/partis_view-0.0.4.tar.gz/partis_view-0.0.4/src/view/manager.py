# -*- coding: UTF-8 -*-

import sys
import os
import re
import time
import trio
import numpy as np

from partis.utils import (
  getLogger )

log = getLogger(__name__)

from PySide2 import QtCore, QtWidgets, QtGui

from .base import (
  QtLogHandler )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Manager( object ):
  """Application manager
  """


  #-----------------------------------------------------------------------------
  def __init__( self,
    main_window_class,
    theme = None,
    init_file = None,
    testing = None,
    logger = None ):
    """Initialization of application manager

    Parameters
    ----------
    main_window_class : class
      main Qt window class.
    theme : None | string
      Name of GUI theme to use.
    init_file : None | string
      Initial directory/file
    testing : None | bool
      Runs automated tests embedded in main_window/widgets
    """

    # applicication initialization values
    self._main_window_class = main_window_class

    # self._init_state = State( "", {
    #   "status" : State("", { "0" : Status.INIT })
    # })

    # self._init_state.update_paths()

    if testing is None:
      testing = False

    testing = bool(testing)

    if logger is None:
      logger = log


    self._logger = logger
    self._state = None
    self._async_nursery = None
    self._async_queue = list()
    self._actions = []
    self._exit = 0
    self._testing = testing
    self._testing_init = testing
    self._testing_queue = list()
    self._testing_num = 0

    # self._reduce = Reducer()

    self._app = QtWidgets.QApplication()
    self._window = self._main_window_class(
      self,
      theme = theme,
      logger = logger )

    if init_file is not None and init_file != "":
      self._window.project.set_root_dir( init_file )

    self._app.setAttribute( QtCore.Qt.AA_UseStyleSheetPropagationInWidgetStyles, True )

    self._qt_log_handler = QtLogHandler(
      logger = self._logger )

    QtCore.qInstallMessageHandler( self._qt_log_handler.qt_message_handler )

  #-----------------------------------------------------------------------------
  @property
  def window(self):
    return self._window

  #-----------------------------------------------------------------------------
  @property
  def app( self ):
    return self._app

  #-----------------------------------------------------------------------------
  @property
  def state(self):
    return self._state

  #-----------------------------------------------------------------------------
  def set_state( self, state ):

    if state is self._state:
      return

    self._state = state

    self.window.set_state( state )

  #-----------------------------------------------------------------------------
  def dispatch( self, action ):

    self._actions.append( action )

  #-----------------------------------------------------------------------------
  def run( self ):
    #args = arg_parser.parse_args()

    self.window.show()

    trio.run( self._async_run )

    self._cleanup()

    return self._exit

  #-----------------------------------------------------------------------------
  def exit( self, value = 0 ):

    self._exit = value
    self._async_nursery.cancel_scope.cancel()

  #-----------------------------------------------------------------------------
  async def _async_run(self):

    async with trio.open_nursery() as nursery:

      self._async_nursery = nursery

      nursery.start_soon( self._state_loop )

      nursery.start_soon( self._gui_loop )

    self._async_nursery = None

  #-----------------------------------------------------------------------------
  async def _state_loop(self):
    """Main state loop
    """

    # self.set_state( self._init_state )

    while True:
      # will exit when nursery is cancelled

      # TODO: remove sleep. any await will throw Cancelled exception upon cancellation
      await trio.sleep(0)

      if len(self._actions) != 0:
        next_state = self._reduce( self._actions, self._state )
        self._actions = []

        self.set_state( next_state )


  #-----------------------------------------------------------------------------
  async def _gui_loop(self):
    """Main gui async event loop
    """

    while True:
      # will exit when nursery is cancelled

      # TODO: remove sleep. any await will throw Cancelled exception upon cancellation
      await trio.sleep(0)

      # process Qt events
      self.app.sendPostedEvents()
      self.app.processEvents()

      while len(self._async_queue) > 0:
        args = self._async_queue.pop(0)
        self._async_nursery.start_soon( self._run_coroutine, args )

      if self._testing:
        if self._testing_init:
          self._testing_init = False
          self.test( self.window )

        if self._testing_num <= 0 and len(self._testing_queue) > 0:
          # run one test at a time
          args = self._testing_queue.pop(0)
          self._async_nursery.start_soon( self._run_test, args )
          self._testing_num += 1

        if self._testing_num <= 0:
          self.exit()

  #-----------------------------------------------------------------------------
  def run_coroutine( self, args ):
    self._async_queue.append( args )

  #-----------------------------------------------------------------------------
  async def _run_coroutine( self, args ):

    try:
      await args[0]( *(args[1:]) )

    except BaseException as e:
      self._logger.error( f"Uncaught exception in co-routine: {args[0]}, args = {args[1:]}", exc_info = True )

  #-----------------------------------------------------------------------------
  def test( self, obj ):
    attrs = dir(obj)

    for attr in attrs:
      f = getattr( obj, attr )

      if callable(f) and attr.startswith('test_'):
        self._logger.info(f"running test: {attr}")
        self._testing_queue.append( [f,] )

  #-----------------------------------------------------------------------------
  async def _run_test( self, args ):

    try:
      await args[0]( *(args[1:]) )

    except BaseException as e:
      self._logger.error( f"test failed: {args[0]}, args = {args[1:]}", exc_info = True )
      self.exit(1)
    finally:
      self._testing_num -= 1

  #-----------------------------------------------------------------------------
  def _cleanup( self ):
    if self._app is None:
      return

    # NOTE: this is done to force the destruction of application object, releasing
    # the reference to the display. If this is not released it can lead to a segmentation
    # fault during testing when a virtual display is used and stops running before
    # the QApplication de-allocates, even if the test completes succesfully.
    # TODO: this seems very fragile, assumes application will actually gets de-allocated
    # by the garbage collector
    self._app.closeAllWindows()
    self._app.exit( self._exit )
    self._app = None
    self._window = None
    import gc
    gc.collect()
